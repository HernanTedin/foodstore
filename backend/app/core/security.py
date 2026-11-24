import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt
from fastapi import Response

from app.core.config import settings

BCRYPT_ROUNDS = 12
ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"
REFRESH_COOKIE_PATH = "/api/v1/auth"


# --- Contraseñas -------------------------------------------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=BCRYPT_ROUNDS)).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Comparación en tiempo constante (la hace bcrypt.checkpw)."""
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except ValueError:
        return False


# Hash fijo para comparar cuando el email no existe y así no revelar, por
# tiempo de respuesta, qué emails están registrados.
DUMMY_HASH = hash_password("dummy-password-para-tiempo-constante")


# --- Access token (JWT) ------------------------------------------------------
def create_access_token(usuario_id: int) -> str:
    ahora = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": str(usuario_id),
        "type": "access",
        "iat": ahora,
        "exp": ahora + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> int | None:
    """Devuelve el id del usuario o None si la firma, la expiración o el tipo fallan."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError:
        return None
    if payload.get("type") != "access" or not str(payload.get("sub", "")).isdigit():
        return None
    return int(payload["sub"])


# --- Refresh token (opaco, se guarda solo su SHA-256) ------------------------
def generate_refresh_token() -> tuple[str, str]:
    """Devuelve (token en claro para la cookie, hash SHA-256 para la base)."""
    token = secrets.token_urlsafe(48)
    return token, hash_refresh_token(token)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def refresh_expiration() -> datetime:
    return datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)


# --- Cookies -----------------------------------------------------------------
def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    common: dict[str, Any] = {
        "httponly": True,
        "samesite": "lax",
        "secure": settings.cookie_secure,
    }
    response.set_cookie(
        ACCESS_COOKIE,
        access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        **common,
    )
    response.set_cookie(
        REFRESH_COOKIE,
        refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path=REFRESH_COOKIE_PATH,
        **common,
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(ACCESS_COOKIE, path="/")
    response.delete_cookie(REFRESH_COOKIE, path=REFRESH_COOKIE_PATH)

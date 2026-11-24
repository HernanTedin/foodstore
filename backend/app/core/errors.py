from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class DomainError(Exception):
    """Error base de negocio. Cada subclase define su status HTTP y su código."""

    status_code: int = 400
    code: str = "domain_error"

    def __init__(self, detail: str, *, field: str | None = None, code: str | None = None):
        super().__init__(detail)
        self.detail = detail
        self.field = field
        if code:
            self.code = code


class NotFoundError(DomainError):
    status_code = 404
    code = "not_found"


class ConflictError(DomainError):
    status_code = 409
    code = "conflict"


class ValidationError(DomainError):
    status_code = 422
    code = "validation_error"


class ForbiddenError(DomainError):
    status_code = 403
    code = "forbidden"


class AuthenticationError(DomainError):
    status_code = 401
    code = "unauthorized"


class AccountStateError(DomainError):
    """400: la cuenta está bloqueada o dada de baja (no es un problema de credenciales)."""

    status_code = 400
    code = "ACCOUNT_DISABLED"


def _body(detail: str, code: str, field: str | None) -> dict:
    return {"detail": detail, "code": code, "field": field}


async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_body(exc.detail, exc.code, exc.field),
    )


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    primero = exc.errors()[0]
    campo = str(primero["loc"][-1]) if primero["loc"] else None
    return JSONResponse(
        status_code=422,
        content=_body(primero["msg"], "validation_error", campo),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, domain_error_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore

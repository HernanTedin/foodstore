import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

SIMBOLOS = re.compile(r"[^A-Za-z0-9]")


def validar_politica_password(password: str) -> str:
    """Mínimo 12 caracteres, una mayúscula, un dígito y un carácter especial.

    También limita a 72 bytes, que es el máximo que procesa bcrypt.
    """
    errores = []
    if len(password) < 12:
        errores.append("al menos 12 caracteres")
    if not any(c.isupper() for c in password):
        errores.append("una mayúscula")
    if not any(c.isdigit() for c in password):
        errores.append("un dígito")
    if not SIMBOLOS.search(password):
        errores.append("un carácter especial")
    if errores:
        raise ValueError("La contraseña debe tener " + ", ".join(errores))
    if len(password.encode()) > 72:
        raise ValueError("La contraseña no puede superar los 72 bytes")
    return password


class RegisterRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=80)
    apellido: str = Field(min_length=1, max_length=80)
    email: EmailStr = Field(max_length=254)
    telefono: str | None = Field(default=None, max_length=30)
    password: str

    _politica = field_validator("password")(validar_politica_password)


class PasswordChangeRequest(BaseModel):
    password_actual: str
    password_nueva: str

    _politica = field_validator("password_nueva")(validar_politica_password)


class UsuarioMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellido: str
    email: str
    telefono: str | None
    roles: list[str]

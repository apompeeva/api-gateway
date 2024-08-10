from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Данные для регистрации."""

    login: str
    password: str


class AuthResponse(BaseModel):
    """Токен."""

    access_token: str

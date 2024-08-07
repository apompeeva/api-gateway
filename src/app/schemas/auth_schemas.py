import requests
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    login: str
    password: str

class AuthResponse(BaseModel):
    access_token: str

from pydantic import BaseModel
import requests

class RegisterRequest(BaseModel):
    login: str
    password: str

class AuthResponse(BaseModel):
    access_token: str

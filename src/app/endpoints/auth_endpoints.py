import httpx
from fastapi import APIRouter, HTTPException, status

from app.schemas.auth_schemas import AuthResponse, RegisterRequest

auth_router = APIRouter()

AUTH_SERVICE_URL = "http://127.0.0.1:8001"

headers = {
    "Content-Type": "application/json",
}


@auth_router.get("/test")
async def test_get():
    response = httpx.get(AUTH_SERVICE_URL + "/test")
    return response.json()


@auth_router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    response = httpx.post(
        AUTH_SERVICE_URL + "/register",
        data=request.model_dump_json(),
        headers=headers,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


@auth_router.post("/auth", response_model=AuthResponse)
async def authorize(request: RegisterRequest):
    response = httpx.post(
        AUTH_SERVICE_URL + "/auth",
        data=request.model_dump_json(),
        headers=headers,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

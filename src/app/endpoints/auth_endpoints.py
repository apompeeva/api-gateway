import httpx
from fastapi import APIRouter, HTTPException, status, UploadFile

from app.schemas.auth_schemas import AuthResponse, RegisterRequest

auth_router = APIRouter()

AUTH_SERVICE_URL = 'http://auth:8001'

headers = {
    'Content-Type': 'application/json',
}


@auth_router.post('/register', response_model=AuthResponse)
async def register(request: RegisterRequest):
    """Проксирует запрос регистрации пользователя."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AUTH_SERVICE_URL + '/register',
            data=request.model_dump_json(),
            headers=headers,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code, detail=response.text,
            )
    return response.json()


@auth_router.post('/auth', response_model=AuthResponse)
async def authorize(request: RegisterRequest):
    """Проксирует запрос авторизации пользователя."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AUTH_SERVICE_URL + '/auth',
            data=request.model_dump_json(),
            headers=headers,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code, detail=response.text,
            )
    return response.json()


@auth_router.post('/api/verify', status_code=status.HTTP_200_OK)
async def verify_user(user_id: int, file: UploadFile):
    """Верификация пользователя."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            AUTH_SERVICE_URL + '/api/verify' + f'?user_id={user_id}',
            headers=headers,
            files={'file': (file.filename, file.file, file.content_type), },
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code, detail=response.text,
            )
    return response.json()

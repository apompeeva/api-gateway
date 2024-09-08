import httpx
from fastapi import APIRouter, HTTPException, UploadFile, status
from opentracing import Format, global_tracer

from app.schemas.auth_schemas import AuthResponse, RegisterRequest

auth_router = APIRouter()

AUTH_SERVICE_URL = 'http://auth-service-pompeeva:8001'

headers = {
    'Content-Type': 'application/json',
}


@auth_router.post('/register', response_model=AuthResponse)
async def register(request: RegisterRequest):
    """Проксирует запрос регистрации пользователя."""
    with global_tracer().start_active_span('register_user') as scope:
        span = global_tracer().active_span
        if span:
            global_tracer().inject(span.context, Format.HTTP_HEADERS, headers)
        scope.span.set_tag('login', request.login)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AUTH_SERVICE_URL + '/register',
                data=request.model_dump_json(),
                headers=headers,
            )
            scope.span.set_tag('response_status', response.status_code)
            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text,
                )
        return response.json()


@auth_router.post('/auth', response_model=AuthResponse)
async def authorize(request: RegisterRequest):
    """Проксирует запрос авторизации пользователя."""
    with global_tracer().start_active_span('authorize_user') as scope:
        span = global_tracer().active_span
        if span:
            global_tracer().inject(span.context, Format.HTTP_HEADERS, headers)
        scope.span.set_tag('login', request.login)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AUTH_SERVICE_URL + '/auth',
                data=request.model_dump_json(),
                headers=headers,
            )
            scope.span.set_tag('response_status', response.status_code)
            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text,
                )
        return response.json()


@auth_router.post('/api/verify', status_code=status.HTTP_200_OK)
async def verify_user(user_id: int, file: UploadFile):
    """Верификация пользователя."""
    with global_tracer().start_active_span('verify_user') as scope:
        span = global_tracer().active_span
        if span:
            global_tracer().inject(span.context, Format.HTTP_HEADERS, headers)
        scope.span.set_tag('user_id', user_id)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AUTH_SERVICE_URL + '/api/verify' + f'?user_id={user_id}',
                files={
                    'file': (
                        file.filename,
                        file.file,
                        file.content_type,
                    ),
                },
            )
            scope.span.set_tag('response_status', response.status_code)
            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text,
                )
        return response.json()

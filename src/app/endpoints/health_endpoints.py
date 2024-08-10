import httpx
from fastapi import APIRouter, HTTPException, status

from app.endpoints.auth_endpoints import AUTH_SERVICE_URL
from app.endpoints.transaction_endpoints import TRANSACTION_SERVICE_URL

health_router = APIRouter()

headers = {
    'Content-Type': 'application/json',
}


@health_router.get('/healthz/ready', status_code=status.HTTP_200_OK)
async def health_check():
    """Проверка доступности сервисов."""
    async with httpx.AsyncClient() as client:
        auth_response = await client.get(AUTH_SERVICE_URL + '/healthz/ready')
        transaction_response = await client.get(
            TRANSACTION_SERVICE_URL + '/healthz/ready',
        )
        if auth_response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        if transaction_response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

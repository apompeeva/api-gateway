from httpx import AsyncClient, Response
from unittest.mock import patch, AsyncMock
from fastapi import status


async def test_health_check(ac: AsyncClient):
    with patch('app.endpoints.auth_endpoints.httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_auth_response = Response(status.HTTP_200_OK)
        mock_get.return_value = mock_auth_response

        with patch('app.endpoints.transaction_endpoints.httpx.AsyncClient.get', new_callable=AsyncMock) as mock_post:
            mock_response = Response(status.HTTP_200_OK)
            mock_post.return_value = mock_response

            response = await ac.get('/healthz/ready')

            assert response.status_code == status.HTTP_200_OK

import pytest
from httpx import AsyncClient, Response
from unittest.mock import patch, AsyncMock


@pytest.mark.parametrize('login, password, expected_response', (
    pytest.param('user', '123pass123', 200, id='new_user'),
    pytest.param('user', '123pass123', 400, id='existed_user')
))
async def test_register(ac: AsyncClient, login, password, expected_response):
    with patch('app.endpoints.auth_endpoints.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        mock_response = Response(expected_response, json={
                                 "token": "test_token"})
        mock_post.return_value = mock_response

        register_data = {
            "login": login,
            "password": password,
        }

        response = await ac.post('/register', json=register_data)

        assert response.status_code == expected_response
        assert response.json() == {"token": "test_token"}


@pytest.mark.parametrize('login, password, expected_response', (
    pytest.param('user_not_exist', '123pass123', 404, id='new_user'),
    pytest.param('user', '123pass123', 200, id='existed_user')
))
async def test_auth(ac: AsyncClient, login, password, expected_response):
    with patch('app.endpoints.auth_endpoints.httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        mock_response = Response(expected_response, json={
                                 "token": "test_token"})
        mock_post.return_value = mock_response
        auth_data = {
            "login": login,
            "password": password,
        }

        response = await ac.post('/auth', json=auth_data)

        assert response.status_code == expected_response


@pytest.mark.parametrize('user_id, expected_response', (
    pytest.param('100', 404, id='not_token'),
    pytest.param('10', 200, id='valid_token'),
    pytest.param('11', 401, id='token_expired')
))
async def test_check_token(ac: AsyncClient, user_id, expected_response):
    with patch('app.endpoints.auth_endpoints.httpx.AsyncClient.get', new_callable=AsyncMock) as mock_post:
        mock_response = Response(expected_response)
        mock_post.return_value = mock_response

        response = await ac.get('/check_token' + f'?user_id={user_id}')

        assert response.status_code == expected_response

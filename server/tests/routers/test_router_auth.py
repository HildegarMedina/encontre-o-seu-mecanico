"""Router Auth test file."""
from config.config import ALGORITHM, SECRET_KEY
import pytest
from app import app
from async_asgi_testclient import TestClient
from jose import jwt

@pytest.mark.asyncio
async def test_authentication():
    """Test the /auth route."""
    headers = {"accept": "application/json"}
    data = {
        "email": "John",
        "password": "123456",
        "type": "client"
    }
    async with TestClient(app) as client:
        response = await client.post("/auth", headers=headers, json=data)
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_me():
    """Test the /auth/me route."""
    to_encode = {'username': 'invalid'}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    # Unauthorized
    async with TestClient(app) as client:
        response = await client.get("/auth/me", headers=headers)
        assert response.status_code == 401
    
    # Invalid token
    async with TestClient(app) as client:
        headers["Authorization"] = 'Bearer token'
        response = await client.get("/auth/me", headers=headers)
        assert response.status_code == 401
        headers["Authorization"] = 'token'
        response = await client.get("/auth/me", headers=headers)
        assert response.status_code == 401


import pytest
from httpx import AsyncClient
from src.app import app

import asyncio

@pytest.mark.asyncio
async def test_root_endpoint():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/")
    # Assert
    assert response.status_code == 200
    # Optionally, check response content if known
    # assert response.json() == {"message": "Hello World"}

"""Service Client test file."""
from domain import model
import pytest
from fastapi import HTTPException
from server.schemas.request.client import CreateClient
from services.client import ClientService
from mockups.clients import clients_mock
from fixtures.client import create_client, destroy_client

@pytest.mark.asyncio
async def test_get_client_by_email(setup):
    """Test the get client by email."""
    repo, client = setup

    # Create client
    client_save = await create_client(clients_mock['john'], model, repo)

    # Get client by email
    client_svc = ClientService(model, repo)
    response = await client_svc.get_client_by_email(client_save['email'])
    assert response['id']

@pytest.mark.asyncio
async def test_register(setup):
    """Test the register."""
    repo, client = setup
    
    # Destroy user in db
    await destroy_client(clients_mock['john'], model, repo)

    # Register
    client_svc = ClientService(model, repo)
    response = await client_svc.register(CreateClient(**clients_mock['john']))
    assert response > 0

@pytest.mark.asyncio
async def test_register_failed(setup):
    """Test the register failed."""
    repo, client = setup

    # Register (User already registered)
    client_svc = ClientService(model, repo)
    with pytest.raises(HTTPException) as exc_info:
        await client_svc.register(CreateClient(**clients_mock['john']))
    assert exc_info.value.detail == 'User already registered'

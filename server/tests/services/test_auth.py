"""Service Auth test file."""
from domain import model
import pytest
from fastapi import HTTPException
from services.auth import AuthService
from mockups.clients import clients_mock
from mockups.mechanics import mechanics_mock
from fixtures.client import create_client
from fixtures.mechanic import create_mechanic

@pytest.mark.asyncio
async def test_create_access_token(setup):
    """Test the create access token."""
    repo, client = setup


    # Create access token
    auth_svc = AuthService(model, repo)
    client_user = clients_mock["john"].copy()
    client_user['id'] = 1
    client_user['permissions'] = ''
    response = auth_svc.create_access_token(client_user)
    assert response['access_token']


@pytest.mark.asyncio
async def test_authenticate_client(setup):
    """Test the authenticate client."""
    repo, client = setup
    
    # Create client
    await create_client(clients_mock['john'] ,model, repo)

    # Auth client
    auth_svc = AuthService(model, repo)
    response = await auth_svc.authenticate(
        clients_mock['john']['email'],
        clients_mock['john']['password'],
        'client'
    )
    assert response['access_token']

@pytest.mark.asyncio
async def test_authenticate_mechanic(setup):
    """Test the authenticate mechanic."""
    repo, client = setup
    
    # Create mechanic
    await create_mechanic(mechanics_mock['john'] ,model, repo)

    # Auth mechanic
    auth_svc = AuthService(model, repo)
    response = await auth_svc.authenticate(
        mechanics_mock['john']['email'],
        mechanics_mock['john']['password'],
        'mechanic'
    )
    assert response['access_token']

@pytest.mark.asyncio
async def test_me_client(setup):
    """Test the me client."""
    repo, client = setup
    
    # Create client
    client_save = await create_client(clients_mock['john'] ,model, repo)

    # Auth client
    auth_svc = AuthService(model, repo)
    response = await auth_svc.authenticate(
        clients_mock['john']['email'],
        clients_mock['john']['password'],
        'client'
    )
    
    # Me client
    me = await auth_svc.me(response['access_token'], 'client')
    assert client_save['id'] == me.id

@pytest.mark.asyncio
async def test_me_mechanic(setup):
    """Test the me mechanic."""
    repo, client = setup
    
    # Create mechanic
    mechanic_save = await create_mechanic(mechanics_mock['john'] ,model, repo)

    # Auth mechanic
    auth_svc = AuthService(model, repo)
    response = await auth_svc.authenticate(
        mechanics_mock['john']['email'],
        mechanics_mock['john']['password'],
        'mechanic'
    )
    
    # Me mechanic
    me = await auth_svc.me(response['access_token'], 'mechanic')
    assert mechanic_save['id'] == me.id

@pytest.mark.asyncio
async def test_me_failed(setup):
    """Test the me failed."""
    repo, client = setup

    # Me client failed
    auth_svc = AuthService(model, repo)
    with pytest.raises(HTTPException) as exc_info:
        await auth_svc.me('accesstokenfailed', 'client')
    assert exc_info.value.detail == 'Could not validate credentials'

    # Me client not found
    client_user = clients_mock["jane"].copy()
    client_user['id'] = 1
    client_user['permissions'] = ''
    response = auth_svc.create_access_token(client_user)
    with pytest.raises(HTTPException) as exc_info:
        await auth_svc.me(response['access_token'], 'client')
    assert exc_info.value.detail == 'Could not validate credentials'

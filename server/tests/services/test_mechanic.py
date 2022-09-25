"""Service Mechanic test file."""
from domain import model
import pytest
from fastapi import HTTPException
from schemas.request.mechanic import CreateMechanic
from services.mechanic import MechanicService
from mockups.mechanics import mechanics_mock
from fixtures.mechanic import create_mechanic, destroy_mechanic

@pytest.mark.asyncio
async def test_get_mechanic_by_email(setup):
    """Test the get mechanic by email."""
    repo, client = setup

    # Create mechanic
    mechanic_save = await create_mechanic(mechanics_mock['john'], model, repo)

    # Get mechanic by email
    mechanic_svc = MechanicService(model, repo)
    response = await mechanic_svc.get_mechanic_by_email(mechanic_save['email'])
    assert response['id']

@pytest.mark.asyncio
async def test_register(setup):
    """Test the register."""
    repo, client = setup
    
    # Destroy user in db
    await destroy_mechanic(mechanics_mock['john'], model, repo)

    # Register
    mechanic_svc = MechanicService(model, repo)
    response = await mechanic_svc.register(CreateMechanic(**mechanics_mock['john']))
    assert response > 0

@pytest.mark.asyncio
async def test_register_failed(setup):
    """Test the register failed."""
    repo, client = setup

    # Register (Mechanic already registered)
    mechanic_svc = MechanicService(model, repo)
    with pytest.raises(HTTPException) as exc_info:
        await mechanic_svc.register(CreateMechanic(**mechanics_mock['john']))
    assert exc_info.value.detail == 'Mechanic already registered'

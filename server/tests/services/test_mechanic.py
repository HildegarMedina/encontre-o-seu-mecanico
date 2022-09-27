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
    
    # Destroy
    await destroy_mechanic(mechanic_save, model, repo)
    
@pytest.mark.asyncio
async def test_get_mechanic_by_id(setup):
    """Test the get mechanic by id."""
    repo, client = setup

    # Create mechanic
    mechanic_save = await create_mechanic(mechanics_mock['john'], model, repo)

    # Get mechanic by id
    mechanic_svc = MechanicService(model, repo)
    response = await mechanic_svc.get_mechanic_by_id(mechanic_save['id'])
    assert response['id'] == mechanic_save['id']
    
    # Destroy
    await destroy_mechanic(mechanic_save, model, repo)

@pytest.mark.asyncio
async def test_get_mechanic_by_id_failed(setup):
    """Test the get mechanic by id failed."""
    repo, client = setup

    # Get mechanic by id
    mechanic_svc = MechanicService(model, repo)
    
    with pytest.raises(HTTPException) as exc_info:
        await mechanic_svc.get_mechanic_by_id(1234)
    assert exc_info.value.detail == 'Mechanic not found'

@pytest.mark.asyncio
async def test_register(setup):
    """Test the register."""
    repo, client = setup

    # Register
    mechanic_svc = MechanicService(model, repo)
    response = await mechanic_svc.register(CreateMechanic(**mechanics_mock['john']))
    assert response > 0
    
    # Destroy
    await destroy_mechanic(mechanics_mock['john'], model, repo)

@pytest.mark.asyncio
async def test_register_failed(setup):
    """Test the register failed."""
    repo, client = setup
    
    await create_mechanic(mechanics_mock['john'], model, repo)

    # Register (Mechanic already registered)
    mechanic_svc = MechanicService(model, repo)
    with pytest.raises(HTTPException) as exc_info:
        await mechanic_svc.register(CreateMechanic(**mechanics_mock['john']))
    assert exc_info.value.detail == 'Mechanic already registered'
    
    # Destroy
    await destroy_mechanic(mechanics_mock['john'], model, repo)

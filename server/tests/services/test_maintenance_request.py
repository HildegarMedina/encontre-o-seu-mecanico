"""Service Maintenance Request test file."""
from domain import model
import pytest
from fastapi import HTTPException
from schemas.request.car import AddCar, UpdateCar
from schemas.response.auth import AccessTokenResponse
from fixtures.admin import create_admin, destroy_admin
from fixtures.maintenance_request import create_maintenance_request, destroy_maintenance_request
from schemas.request.maintenance_request import CreateMaintenanceRequest, UpdateMaintenanceRequest
from services.maintenance_request import MaintenanceRequestService
from mockups.clients import clients_mock
from mockups.car import cars_mock
from mockups.maintenance_request import maintenance_request_mock
from mockups.mechanics import mechanics_mock
from fixtures.client import create_client, destroy_client
from fixtures.car import create_car, destroy_car
from fixtures.mechanic import create_mechanic, destroy_mechanic

@pytest.mark.asyncio
async def test_get_list(setup): 
    """Test the get list cars."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)
    
    # Create maintenance request
    m_request_mock = maintenance_request_mock['open'].copy()
    m_request_mock["car"] = car_save["id"]
    await create_maintenance_request(m_request_mock, model, repo, client_save)

    # Get list
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**client_save))
    response = await m_request_svc.get_list()
    assert len(response) > 0
    
    # Destroy car
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_save, model, repo)

@pytest.mark.asyncio
async def test_get_list_all(setup):
    """Test the get list cars."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_admin(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)
    
    # Create maintenance request
    m_request_mock = maintenance_request_mock['open'].copy()
    m_request_mock["car"] = car_save["id"]
    await create_maintenance_request(m_request_mock, model, repo, client_save)

    # Get list
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**client_save))
    response = await m_request_svc.get_list(True)
    assert len(response) > 0
    
    # Destroy car
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_admin(client_save, model, repo)

@pytest.mark.asyncio
async def test_get_maintenance_request_by_id(setup):
    """Test the get car by id."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)
    
    # Create maintenance request
    m_request_mock = maintenance_request_mock['open'].copy()
    m_request_mock["car"] = car_save["id"]
    m_request_save = await create_maintenance_request(m_request_mock, model, repo, client_save)

    # Get maintenance request by id
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**client_save))
    response = await m_request_svc.get_maintenance_request_by_id(m_request_save["id"])
    assert response.id == m_request_save["id"]
    
    # Destroy car
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_save, model, repo)

@pytest.mark.asyncio
async def test_get_maintenance_request_by_id_failed(setup):
    """Test the get car by id failed."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Get maintenance request by id
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**client_save))
    with pytest.raises(HTTPException) as exc_info:
        await m_request_svc.get_maintenance_request_by_id(1234)
    assert exc_info.value.detail == 'Maintenance request not found'

    # Destroy car
    await destroy_client(client_save, model, repo)


@pytest.mark.asyncio
async def test_create(setup):
    """Test the create."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)
    
    # Create mechanic
    mechanic_save = await create_mechanic(mechanics_mock['john'], model, repo)
    
    # Create maintenance request
    m_request_mock = maintenance_request_mock['open'].copy()
    m_request_mock["car"] = car_save["id"]
    m_request_mock["mechanic"] = mechanic_save["id"]
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**client_save))
    response_id = await m_request_svc.create(CreateMaintenanceRequest(**m_request_mock))
    assert response_id > 0

    # Destroy
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_maintenance_request(response_id, model, repo, client_save)
    await destroy_client(client_save, model, repo)
    await destroy_mechanic(mechanic_save, model, repo)

@pytest.mark.asyncio
async def test_create_failed(setup):
    """Test the create failed."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)
    
    # Create maintenance request
    m_request_mock = maintenance_request_mock['open'].copy()
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**client_save))
    with pytest.raises(HTTPException) as exc_info:
        await m_request_svc.create(CreateMaintenanceRequest(**m_request_mock))
    assert exc_info.value.detail == 'Car not found'

    # Destroy
    await destroy_client(client_save, model, repo)


@pytest.mark.asyncio
async def test_update_request(setup):
    """Test the Update request."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)
    
    # Create mechanic
    mechanic_save = await create_mechanic(mechanics_mock['john'], model, repo)

    # Create maintenance request
    m_request_mock = maintenance_request_mock['open'].copy()
    m_request_mock["car"] = car_save["id"]
    m_request_mock["mechanic"] = mechanic_save["id"]
    m_request_save = await create_maintenance_request(m_request_mock, model, repo, client_save)
    
    # Update maintenance request
    m_request_mock["id"] = m_request_save["id"]
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**client_save))
    response = await m_request_svc.update_request(UpdateMaintenanceRequest(**m_request_mock))
    assert response == None

    # Destroy
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_maintenance_request(m_request_save["id"], model, repo, client_save)
    await destroy_client(client_save, model, repo)
    await destroy_mechanic(mechanic_save, model, repo)


@pytest.mark.asyncio
async def test_update_request_failed(setup):
    """Test the update request failed."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Update maintenance request
    m_request_mock = maintenance_request_mock['open'].copy()
    m_request_mock["id"] = 1234
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**client_save))
    with pytest.raises(HTTPException) as exc_info:
        await m_request_svc.update_request(UpdateMaintenanceRequest(**m_request_mock))
    assert exc_info.value.detail == 'Maintenance request not found'

    # Destroy
    await destroy_client(client_save, model, repo)

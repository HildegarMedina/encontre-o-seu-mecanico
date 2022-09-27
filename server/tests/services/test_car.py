"""Service Car test file."""
from domain import model
import pytest
from fastapi import HTTPException
from schemas.request.car import AddCar, UpdateCar
from schemas.response.auth import AccessTokenResponse
from tests.fixtures.admin import create_admin, destroy_admin
from services.car import CarService
from mockups.clients import clients_mock
from mockups.car import cars_mock
from fixtures.client import create_client, destroy_client
from fixtures.car import create_car, destroy_car

@pytest.mark.asyncio
async def test_get_list(setup):
    """Test the get list cars."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Get list
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    response = await car_svc.get_list()
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
    await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Get list
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    response = await car_svc.get_list(True)
    assert len(response) > 0

    # Destroy car
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_admin(client_save, model, repo)

@pytest.mark.asyncio
async def test_get_car_by_id(setup):
    """Test the get car by id."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Get car by id
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    response = await car_svc.get_car_by_id(car_save["id"])
    assert response["id"] == car_save["id"]
    
    # Destroy car
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)

@pytest.mark.asyncio
async def test_get_car_by_id_failed(setup):
    """Test the get car by id failed."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Get car by id
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    with pytest.raises(HTTPException) as exc_info:
        await car_svc.get_car_by_id(1234)
    assert exc_info.value.detail == 'Car not found'
    
    # Destroy car
    await destroy_client(client_mock, model, repo)

@pytest.mark.asyncio
async def test_get_car_by_details(setup):
    """Test the get car by details."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Get car by details
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    response = await car_svc.get_car_by_details(car_save["brand"], car_save["model"],
                                                car_save["version"], car_save["year"], client_save["id"])
    assert response["id"] == car_save["id"]
    
    # Destroy car
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)


@pytest.mark.asyncio
async def test_add(setup):
    """Test the add."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Add car
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    response = await car_svc.add(AddCar(**cars_mock["vw/gol"]))
    assert response > 0
    
    # Destroy car
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)

@pytest.mark.asyncio
async def test_add_failed(setup):
    """Test the add failed."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Add car failed
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    with pytest.raises(HTTPException) as exc_info:
        await car_svc.add(AddCar(**cars_mock["vw/gol"]))
    assert exc_info.value.detail == 'Car already registered'
    
    # Destroy car
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)


@pytest.mark.asyncio
async def test_change_details(setup):
    """Test the change details."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)
    
    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Change details
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    car_mock = cars_mock["fiat/palio"].copy()
    car_mock['id'] = car_save['id']
    response = await car_svc.change_details(UpdateCar(**car_mock))
    assert response == None

    # Destroy car
    await destroy_car(cars_mock["fiat/palio"], client_save, model, repo)


@pytest.mark.asyncio
async def test_change_details_failed(setup):
    """Test the change details failed."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)
    
    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Change details
    car_svc = CarService(model, repo, AccessTokenResponse(**client_save))
    car_mock = cars_mock["vw/gol"].copy()
    car_mock['id'] = car_save['id']

    with pytest.raises(HTTPException) as exc_info:
        await car_svc.change_details(UpdateCar(**car_mock))
    assert exc_info.value.detail == 'Car already registered'

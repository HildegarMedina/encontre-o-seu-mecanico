"""Router Car test file."""
import pytest
from domain import model
from mockups.car import cars_mock
from mockups.clients import clients_mock
from fixtures.client import create_client, authenticate_client
from fixtures.car import create_car

@pytest.mark.asyncio
async def test_add_car(setup):
    """Test the /car post route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    await create_client(client_mock, model, repo)
    
    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.post("/car", headers=headers, json=cars_mock["vw/gol"])
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_car_by_id(setup):
    """Test the /car/{id} get route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)
    
    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.get(f"/car/{car_save['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()['id'] == car_save['id']

@pytest.mark.asyncio
async def test_get_cars(setup):
    """Test the /car/ get route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)
    
    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.get("/car", headers=headers)
    assert response.status_code == 200
    assert response.json()[0]['id'] == car_save['id']

@pytest.mark.asyncio
async def test_update_car(setup):
    """Test the /car put route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)
    
    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }
    
    # Payload
    payload = cars_mock["fiat/palio"].copy()
    payload["id"] = car_save["id"]

    response = await client.put("/car", headers=headers, json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_car(setup):
    """Test the /car delete route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.delete(f"/car/{car_save['id']}", headers=headers)
    assert response.status_code == 204

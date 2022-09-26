"""Router Car test file."""
import pytest
from domain import model
from mockups.car import cars_mock
from mockups.mechanics import mechanics_mock
from mockups.clients import clients_mock
from fixtures.client import create_client, authenticate_client, destroy_client
from fixtures.mechanic import create_mechanic, authenticate_mechanic, destroy_mechanic
from fixtures.car import create_car, destroy_car

@pytest.mark.asyncio
async def test_add_car(setup):
    """Test the /car post route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)
    
    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.post("/car", headers=headers, json=cars_mock["vw/gol"])
    assert response.status_code == 201

    # Destroy data
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_mock, model, repo)


@pytest.mark.asyncio
async def test_add_car_without_permissions(setup):
    """Test the /car post failed route."""
    repo, client = setup

    # Create mechanic
    mechanic_mock = mechanics_mock["john"].copy()
    await create_mechanic(mechanic_mock, model, repo)
    
    # Auth mechanic
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.post("/car", headers=headers, json=cars_mock["vw/gol"])
    assert response.status_code == 401
    
    # Destroy
    await destroy_mechanic(mechanic_mock, model, repo)


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
    
    # Destroy data
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_mock, model, repo)


@pytest.mark.asyncio
async def test_get_car_by_id_without_permissions(setup):
    """Test the  /car/{id} get failed route."""
    repo, client = setup

    # Create mechanic
    mechanic_mock = mechanics_mock["john"].copy()
    mechanic_save = await create_mechanic(mechanic_mock, model, repo)
    
    # Auth mechanic
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.get("/car/1", headers=headers)
    assert response.status_code == 401
    
    # Destroy
    await destroy_mechanic(mechanic_mock, model, repo)


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
    
    # Destroy data
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_mock, model, repo)


@pytest.mark.asyncio
async def test_get_cars_without_permissions(setup):
    """Test the  /car get failed route."""
    repo, client = setup

    # Create mechanic
    mechanic_mock = mechanics_mock["john"].copy()
    await create_mechanic(mechanic_mock, model, repo)

    # Auth mechanic
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.get("/car", headers=headers)
    assert response.status_code == 401

    # Destroy
    await destroy_mechanic(mechanic_mock, model, repo)


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
    
    # Destroy data
    await destroy_car(cars_mock["fiat/palio"], client_save, model, repo)
    await destroy_client(client_mock, model, repo)


@pytest.mark.asyncio
async def test_update_car_without_permissions(setup):
    """Test the  /car put failed route."""
    repo, client = setup

    # Create mechanic
    mechanic_mock = mechanics_mock["john"].copy()
    await create_mechanic(mechanic_mock, model, repo)

    # Auth mechanic
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    # Payload
    payload = cars_mock["fiat/palio"].copy()
    payload["id"] = 1

    response = await client.put("/car", headers=headers, json=payload)
    assert response.status_code == 401

    # Destroy data
    await destroy_mechanic(mechanic_mock, model, repo)


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
    
    # Destroy data
    await destroy_client(client_mock, model, repo)


@pytest.mark.asyncio
async def test_delete_car_without_permissions(setup):
    """Test the  /car delete failed route."""
    repo, client = setup

    # Create mechanic
    mechanic_mock = mechanics_mock["john"].copy()
    await create_mechanic(mechanic_mock, model, repo)

    # Auth mechanic
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.delete("/car/1", headers=headers)
    assert response.status_code == 401

    # Destroy
    await destroy_mechanic(mechanic_mock, model, repo)

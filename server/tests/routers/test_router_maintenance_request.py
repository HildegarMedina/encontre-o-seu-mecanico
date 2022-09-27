"""Router Maintenance Request test file."""
import pytest
from domain import model
from mockups.car import cars_mock
from mockups.mechanics import mechanics_mock
from mockups.maintenance_request import maintenance_request_mock
from mockups.clients import clients_mock
from fixtures.client import create_client, authenticate_client, destroy_client
from fixtures.mechanic import create_mechanic, authenticate_mechanic, destroy_mechanic
from fixtures.car import create_car, destroy_car
from server.tests.fixtures.maintenance_request import create_maintenance_request, destroy_maintenance_request

@pytest.mark.asyncio
async def test_create_maintenance_request(setup):
    """Test the /maintenance_request post route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    # Mock maintenance request
    m_req = maintenance_request_mock['open'].copy()
    m_req["car"] = car_save['id']

    response = await client.post("/maintenance_request", headers=headers, json=m_req)
    assert response.status_code == 201

    # Destroy data
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_mock, model, repo)


@pytest.mark.asyncio
async def test_create_maintenance_request_without_permissions(setup):
    """Test the /maintenance_request post failed route."""
    repo, client = setup

    # Create mechanic
    mechanic_mock = mechanics_mock["john"].copy()
    await create_mechanic(mechanic_mock, model, repo)

    # Auth cliente
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.post("/maintenance_request", headers=headers, json=maintenance_request_mock['open'])
    assert response.status_code == 401

    # Destroy data
    await destroy_mechanic(mechanic_mock, model, repo)


@pytest.mark.asyncio
async def test_get_maintenance_request_by_id(setup):
    """Test the /maintenance_request/{id} get route."""
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

    response = await client.get("/maintenance_request/1", headers=headers)
    assert response.status_code == 404

    # Destroy data
    await destroy_client(client_mock, model, repo)


@pytest.mark.asyncio
async def test_get_maintenance_request_without_permissions(setup):
    """Test the  /maintenance_request/{id} get failed route."""
    repo, client = setup

    # Create user
    mechanic_mock = mechanics_mock["john"].copy()
    await create_mechanic(mechanic_mock, model, repo)

    # Auth cliente
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.get("/maintenance_request/1", headers=headers)
    assert response.status_code == 401

    # Destroy data
    await destroy_mechanic(mechanic_mock, model, repo)


@pytest.mark.asyncio
async def test_get_maintenance_requests(setup):
    """Test the /maintenance_request/ get route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.get("/maintenance_request", headers=headers)
    assert response.status_code == 200

    # Destroy data
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_mock, model, repo)


@pytest.mark.asyncio
async def test_get_cars_without_permissions(setup):
    """Test the  /car get failed route."""
    repo, client = setup

    # Create user
    mechanic_mock = mechanics_mock["john"].copy()
    await create_mechanic(mechanic_mock, model, repo)

    # Auth cliente
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.get("/maintenance_request", headers=headers)
    assert response.status_code == 401

    # Destroy data
    await destroy_mechanic(mechanic_mock, model, repo)


@pytest.mark.asyncio
async def test_update_maintenance_request(setup):
    """Test the /maintenance_request put route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }
    
    # Create maintenance request

    # Mock maintenance request
    m_req = maintenance_request_mock['open'].copy()
    m_req["car"] = car_save['id']
    maintenance_request = await create_maintenance_request(m_req, model, repo, client_save)
    m_req["id"] = maintenance_request['id']

    response = await client.put("/maintenance_request", headers=headers, json=m_req)
    assert response.status_code == 204

    # Destroy data
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_mock, model, repo)
    await destroy_maintenance_request(maintenance_request["id"], model, repo, client_save)


@pytest.mark.asyncio
async def test_update_maintenance_request_without_permissions(setup):
    """Test the  /maintenance_request put failed route."""
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
    

    # Mock maintenance request
    m_req = maintenance_request_mock['open'].copy()
    m_req["car"] = 0
    m_req["id"] = 0

    response = await client.put("/maintenance_request", headers=headers, json=m_req)
    assert response.status_code == 401

    # Destroy data
    await destroy_mechanic(mechanic_mock, model, repo)


@pytest.mark.asyncio
async def test_delete_maintenance_request(setup):
    """Test the /maintenance_request delete route."""
    repo, client = setup

    # Create user
    client_mock = clients_mock["john"].copy()
    client_save = await create_client(client_mock, model, repo)

    # Create car
    car_save = await create_car(cars_mock["vw/gol"], client_save, model, repo)

    # Auth cliente
    auth = await authenticate_client(client_mock["email"], client_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }
    
    # Create maintenance request
    m_req = maintenance_request_mock['open'].copy()
    m_req["car"] = car_save['id']
    maintenance_request = await create_maintenance_request(m_req, model, repo, client_save)

    response = await client.delete(
        f"/maintenance_request/{maintenance_request['id']}", 
        headers=headers
    )
    assert response.status_code == 204

    # Destroy data
    await destroy_car(cars_mock["vw/gol"], client_save, model, repo)
    await destroy_client(client_mock, model, repo)

@pytest.mark.asyncio
async def test_delete_maintenance_request_without_permissions(setup):
    """Test the  /maintenance_request delete failed route."""
    repo, client = setup

    # Create user
    mechanic_mock = mechanics_mock["john"].copy()
    await create_mechanic(mechanic_mock, model, repo)

    # Auth mechanic
    auth = await authenticate_mechanic(mechanic_mock["email"], mechanic_mock["password"], model, repo)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + auth["access_token"]
    }

    response = await client.delete("/maintenance_request/1", headers=headers)
    assert response.status_code == 401

    # Destroy data
    await destroy_mechanic(mechanic_mock, model, repo)

from fastapi import APIRouter, Header
from domain import model
from schemas.request.car import AddCar, UpdateCar
from utils.auth import get_user_auth, verify_permissions
from services.car import CarService
from database.db import db
from repository.sql import Repository
repo = Repository(db)

router = APIRouter(
    prefix="/car",
    tags=["Car"]
)

@router.get('')
async def my_cars(Authorization: str = Header(...),):
    """Get all cars."""
    actor = await get_user_auth(Authorization, 'client')
    verify_permissions(actor.permissions, "MANAGE_CARS")
    car_svc = CarService(model, repo, actor)
    return await car_svc.get_list()

@router.get('/{id}')
async def get_car_by_id(id: int, Authorization: str = Header(...),):
    """Get car by id."""
    actor = await get_user_auth(Authorization, 'client')
    verify_permissions(actor.permissions, "MANAGE_CARS")
    car_svc = CarService(model, repo, actor)
    return await car_svc.get_car_by_id(id)

@router.post('', status_code=201)
async def add_car(car: AddCar,  Authorization: str = Header(...),):
    """Add a new car."""
    actor = await get_user_auth(Authorization, 'client')
    verify_permissions(actor.permissions, "MANAGE_CARS")
    car_svc = CarService(model, repo, actor)
    return await car_svc.add(car)

@router.put('')
async def update_car(car: UpdateCar,  Authorization: str = Header(...),):
    """Update a car."""
    actor = await get_user_auth(Authorization, 'client')
    verify_permissions(actor.permissions, "MANAGE_CARS")
    car_svc = CarService(model, repo, actor)
    return await car_svc.change_details(car)

@router.delete('/{id}', status_code=204)
async def delete_car(id: int, Authorization: str = Header(...),):
    """Delete car by id."""
    actor = await get_user_auth(Authorization, 'client')
    verify_permissions(actor.permissions, "MANAGE_CARS")
    car_svc = CarService(model, repo, actor)
    return await car_svc.delete(id)

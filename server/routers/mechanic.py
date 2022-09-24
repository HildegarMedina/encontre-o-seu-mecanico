from fastapi import APIRouter
from domain import model
from schemas.request.mechanic import CreateMechanic
from services.mechanic import MechanicService
from database.db import db
from repository.sql import Repository
repo = Repository(db)

router = APIRouter(
    prefix="/mechanic",
    tags=["Mechanic"]
)

@router.post('', status_code=201)
async def register_new_mechanic(mechanic: CreateMechanic):
    """Create a new mechanic."""
    mechanic_svc = MechanicService(model, repo)
    return await mechanic_svc.register(mechanic)
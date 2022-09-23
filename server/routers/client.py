from fastapi import APIRouter
from domain import model
from schemas.request.client import CreateClient
from services.client import ClientService
from database.db import db
from repository.sql import Repository
repo = Repository(db)

router = APIRouter(
    prefix="/client",
    tags=["Client"]
)

@router.post('', status_code=201)
async def register_new_client(client: CreateClient):
    """Create a new client."""
    client_svc = ClientService(model, repo)
    return await client_svc.register(client)
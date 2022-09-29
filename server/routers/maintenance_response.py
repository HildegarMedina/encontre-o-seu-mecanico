from fastapi import APIRouter, Header
from domain import model
from schemas.request.maintenance_response import CreateMaintenanceResponse, UpdateMaintenanceResponse
from utils.auth import get_user_auth, has_permissions
from services.maintenance_response import MaintenanceResponseService
from database.db import db
from repository.sql import Repository
repo = Repository(db)

router = APIRouter(
    prefix="/maintenance_response",
    tags=["Maintenance Response"]
)

@router.get('')
async def my_maintenance_responses(all: str = False, Authorization: str = Header(...),):
    """Get all maintenance responses."""
    actor = await get_user_auth(Authorization, 'mechanic')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_RESPONSE")
    maintenance_response_svc = MaintenanceResponseService(model, repo, actor)
    return await maintenance_response_svc.get_list(all)

@router.get('/{id}')
async def get_maintenance_response_by_id(id: int, Authorization: str = Header(...),):
    """Get maintenance_response by id."""
    actor = await get_user_auth(Authorization, 'mechanic')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_RESPONSE")
    maintenance_response_svc = MaintenanceResponseService(model, repo, actor)
    return await maintenance_response_svc.get_maintenance_response_by_id(id)

@router.post('', status_code=201)
async def create_maintenance_response(
    maintenance_response: CreateMaintenanceResponse,
    Authorization: str = Header(...)
):
    """Create a maintenance response."""
    actor = await get_user_auth(Authorization, 'mechanic')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_RESPONSE")
    maintenance_response_svc = MaintenanceResponseService(model, repo, actor)
    return await maintenance_response_svc.create(maintenance_response)

@router.put('', status_code=204)
async def update_maintenance_response(
    maintenance_response:  UpdateMaintenanceResponse,
    Authorization: str = Header(...)
):
    """Update a maintenance response."""
    actor = await get_user_auth(Authorization, 'mechanic')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_RESPONSE")
    maintenance_response_svc = MaintenanceResponseService(model, repo, actor)
    return await maintenance_response_svc.update_response(maintenance_response)

@router.delete('/{id}', status_code=204)
async def delete_maintenance_response(id: int, Authorization: str = Header(...)):
    """Delete a maintenance response."""
    actor = await get_user_auth(Authorization, 'mechanic')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_RESPONSE")
    maintenance_response_svc = MaintenanceResponseService(model, repo, actor)
    return await maintenance_response_svc.delete(id)

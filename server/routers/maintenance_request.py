from fastapi import APIRouter, Header
from domain import model
from schemas.request.maintenance_request import CreateMaintenanceRequest, UpdateMaintenanceRequest
from utils.auth import get_user_auth, has_permissions
from services.maintenance_request import MaintenanceRequestService
from database.db import db
from repository.sql import Repository
repo = Repository(db)

router = APIRouter(
    prefix="/maintenance_request",
    tags=["Maintenance Request"]
)

@router.get('')
async def my_maintenance_requests(all: str = False, Authorization: str = Header(...),):
    """Get all maintenance requests."""
    actor = await get_user_auth(Authorization, 'client')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_REQUEST")
    maintenance_request_svc = MaintenanceRequestService(model, repo, actor)
    return await maintenance_request_svc.get_list(all)

@router.get('/{id}')
async def get_maintenance_request_by_id(id: int, Authorization: str = Header(...),):
    """Get maintenance_request by id."""
    actor = await get_user_auth(Authorization, 'client')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_REQUEST")
    maintenance_request_svc = MaintenanceRequestService(model, repo, actor)
    return await maintenance_request_svc.get_maintenance_request_by_id(id)

@router.post('', status_code=201)
async def create_maintenance_request(
    maintenance_request: CreateMaintenanceRequest,
    Authorization: str = Header(...)
):
    """Create a maintenance request."""
    actor = await get_user_auth(Authorization, 'client')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_REQUEST")
    maintenance_request_svc = MaintenanceRequestService(model, repo, actor)
    return await maintenance_request_svc.create(maintenance_request)

@router.put('', status_code=204)
async def update_maintenance_request(
    maintenance_request:  UpdateMaintenanceRequest,
    Authorization: str = Header(...)
):
    """Update a maintenance request."""
    actor = await get_user_auth(Authorization, 'client')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_REQUEST")
    maintenance_request_svc = MaintenanceRequestService(model, repo, actor)
    return await maintenance_request_svc.update_request(maintenance_request)

@router.delete('/{id}', status_code=204)
async def delete_maintenance_request(id: int, Authorization: str = Header(...)):
    """Delete a maintenance request."""
    actor = await get_user_auth(Authorization, 'client')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_REQUEST")
    maintenance_request_svc = MaintenanceRequestService(model, repo, actor)
    return await maintenance_request_svc.delete(id)

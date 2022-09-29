from typing import Literal
from fastapi import APIRouter, Header
from domain import model
from schemas.request.maintenance_request import CreateMaintenanceRequest, UpdateMaintenanceRequest
from utils.auth import get_user_auth, has_permissions
from services.maintenance_request import MaintenanceRequestService
from database.db import db
from repository.sql import Repository
from config.config import STATUS_MAINTENANCE_RESPONSE_ALLOWED
repo = Repository(db)

router = APIRouter(
    prefix="/maintenance_request",
    tags=["Maintenance Request"]
)

@router.get('/status/{status}')
async def all_maintenance_requests_by_status(
    status: Literal[STATUS_MAINTENANCE_RESPONSE_ALLOWED],
    Authorization: str = Header(...)
):
    """Get all maintenance requests status."""
    actor = await get_user_auth(Authorization, 'mechanic')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_RESPONSE")
    maintenance_request_svc = MaintenanceRequestService(model, repo, actor)
    return await maintenance_request_svc.get_list_by_status(status)

@router.get('')
async def my_maintenance_requests(all: str = False, Authorization: str = Header(...)):
    """Get all maintenance requests."""
    actor = await get_user_auth(Authorization, 'client')
    has_permissions(actor.permissions, "MANAGE_MAINTENANCE_REQUEST")
    maintenance_request_svc = MaintenanceRequestService(model, repo, actor)
    return await maintenance_request_svc.get_list(all)

@router.get('/{id}')
async def get_maintenance_request_by_id(id: int, Authorization: str = Header(...)):
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

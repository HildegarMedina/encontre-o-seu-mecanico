from services.maintenance_request import MaintenanceRequestService
from schemas.request.maintenance_request import CreateMaintenanceRequest
from schemas.response.auth import AccessTokenResponse

async def create_maintenance_request(m_request, model, repo, actor):
    m_request_svc = MaintenanceRequestService(model, repo, AccessTokenResponse(**actor))
    await m_request_svc.save(CreateMaintenanceRequest(**m_request))
    m_request = await m_request_svc.get_list()
    return dict(m_request[0])

async def destroy_maintenance_request(id, model, repo, actor):
    m_request_svc = MaintenanceRequestService(model, repo,  AccessTokenResponse(**actor))
    return await m_request_svc.delete(id)

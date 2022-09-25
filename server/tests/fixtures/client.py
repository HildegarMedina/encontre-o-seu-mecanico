from services.client import ClientService
from schemas.request.client import CreateClient

async def create_client(client, model, repo):
    client_svc = ClientService(model, repo)
    await client_svc.save(CreateClient(**client))
    client = await client_svc.get_client_by_email(client['email'])
    return dict(client)

async def destroy_client(client, model, repo):
    client_svc = ClientService(model, repo)
    client = await client_svc.get_client_by_email(client['email'])
    await client_svc.delete(client["id"])

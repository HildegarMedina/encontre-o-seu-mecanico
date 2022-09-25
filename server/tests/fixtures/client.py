from services.client import ClientService
from services.auth import AuthService
from schemas.request.client import CreateClient

async def create_client(client, model, repo):
    client_svc = ClientService(model, repo)
    await client_svc.save(CreateClient(**client))
    client = await client_svc.get_client_by_email(client['email'])
    return dict(client)

async def authenticate_client(email, password, model, repo):
    auth_svc = AuthService(model, repo)
    return await auth_svc.authenticate(email, password, 'client')

async def destroy_client(client, model, repo):
    client_svc = ClientService(model, repo)
    client = await client_svc.get_client_by_email(client['email'])
    await client_svc.delete(client["id"])

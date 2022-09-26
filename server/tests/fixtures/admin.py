from datetime import datetime
from utils.auth import get_password_hash
from services.client import ClientService
from services.auth import AuthService
from schemas.request.client import CreateClient

async def create_admin(client, model, repo):
    client_svc = ClientService(model, repo)
    sql = """INSERT INTO clients (full_name, email, zip_code, password, country, state, city, 
            address, complement, phone, identification, created_at, profile) 
            VALUES(:full_name, :email, :zip_code, :password, :country, :state, :city, :address, :complement, 
            :phone, :identification, :created_at, :profile)"""
    values = {
        "full_name": client["full_name"],
        "email": client["email"],
        "password": get_password_hash(client["password"]),
        "zip_code": client["zip_code"],
        "country": client["country"],
        "state": client["state"],
        "city": client["city"],
        "address": client["address"],
        "complement": client["complement"],
        "phone": client["phone"],
        "identification": client["identification"],
        "created_at": datetime.now(),
        "profile": 1
    }
    await repo.execute(sql, values)
    client = await client_svc.get_client_by_email(client['email'])
    return dict(client)

async def destroy_admin(client, model, repo):
    client_svc = ClientService(model, repo)
    client = await client_svc.get_client_by_email(client['email'])
    await client_svc.delete(client["id"])

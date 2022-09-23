"""Client Service."""
from datetime import datetime
from fastapi import HTTPException

from utils.auth import get_password_hash

class ClientService():

    def __init__(self, model, repo):
        self.model = model
        self.repo = repo
    
    async def get_client_by_email(self, email):
        sql = "SELECT * FROM clients WHERE email = :email"
        values = {"email": email}
        return await self.repo.fetch_one(sql, values)

    async def register(self, client):
        find_client = await self.get_client_by_email(client.email)
        if not find_client:
            await self.save(client)
            client = await self.get_client_by_email(client.email)
            return client.id
        raise HTTPException(200, "User already registered")

    async def save(self, client):
        sql = """INSERT INTO clients (full_name, email, zip_code, password, country, state, city, 
        address, complement, phone, identification,created_at) 
        VALUES(:full_name, :email, :zip_code, :password, :country, :state, :city, :address, :complement, 
        :phone, :identification,:created_at)"""
        values = {
            "full_name": client.full_name,
            "email": client.email,
            "password": get_password_hash(client.password),
            "zip_code": client.zip_code,
            "country": client.country,
            "state": client.state,
            "city": client.city,
            "address": client.address,
            "complement": client.complement,
            "phone": client.phone,
            "identification": client.identification,
            "created_at": datetime.now()
        }
        return await self.repo.execute(sql, values)

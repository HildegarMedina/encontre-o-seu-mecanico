"""Mechanic Service."""
from datetime import datetime
from fastapi import HTTPException
import json
from utils.auth import get_password_hash

class MechanicService():

    def __init__(self, model, repo):
        self.model = model
        self.repo = repo

    async def get_mechanic_by_email(self, email):
        sql = """
            SELECT 
                m.*, p.permissions, p.name as profile 
            FROM 
                mechanics m 
            JOIN 
                profiles p ON p.id = m.profile 
            WHERE 
                m.email = :email"""
        values = {"email": email}
        mechanic = await self.repo.fetch_one(sql, values)
        if mechanic:
            mechanic = dict(mechanic)
            mechanic["services"] = mechanic["services"].replace("\'", "\"")
            mechanic["services"] = json.loads(mechanic["services"])
        return mechanic

    async def get_mechanic_by_id(self, id):
        sql = """
            SELECT 
                m.*, p.permissions, p.name as profile 
            FROM 
                mechanics m 
            JOIN 
                profiles p ON p.id = m.profile 
            WHERE 
                m.id = :id"""
        values = {"id": id}
        mechanic = await self.repo.fetch_one(sql, values)
        if not mechanic:
            raise HTTPException(404, 'Mechanic not found')
        mechanic = dict(mechanic)
        mechanic["services"] = mechanic["services"].replace("\'", "\"")
        mechanic["services"] = json.loads(mechanic["services"])
        return mechanic

    async def register(self, mechanic):
        find_mechanic = await self.get_mechanic_by_email(mechanic.email)
        if not find_mechanic:
            await self.save(mechanic)
            mechanic = await self.get_mechanic_by_email(mechanic.email)
            return mechanic["id"]
        raise HTTPException(409, "Mechanic already registered")

    async def save(self, mechanic):
        sql = """INSERT INTO mechanics (company_logo, company_name, full_name, email, zip_code, password, 
        country, state, city, address, complement, phone, identification,created_at, services, profile) 
        VALUES(:company_logo, :company_name, :full_name, :email, :zip_code, :password, :country, :state, :city, 
        :address, :complement, :phone, :identification,:created_at, :services, :profile)"""
        values = {
            "company_logo": mechanic.company_logo,
            "company_name": mechanic.company_name,
            "full_name": mechanic.full_name,
            "email": mechanic.email,
            "password": get_password_hash(mechanic.password),
            "zip_code": mechanic.zip_code,
            "country": mechanic.country,
            "state": mechanic.state,
            "city": mechanic.city,
            "address": mechanic.address,
            "complement": mechanic.complement,
            "phone": mechanic.phone,
            "identification": mechanic.identification,
            "created_at": datetime.now(),
            "services": str(mechanic.services),
            "profile": 3
        }
        return await self.repo.execute(sql, values)

    async def delete(self, id):
        sql = """DELETE FROM mechanics WHERE id = :id"""
        values = {
            "id": id,
        }
        return await self.repo.execute(sql, values)

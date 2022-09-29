"""Maintenance Response Service."""
from fastapi import HTTPException
from schemas.request.maintenance_response import CreateMaintenanceResponse, UpdateMaintenanceResponse
from services.car import CarService
from services.mechanic import MechanicService
from utils.auth import has_permissions
from datetime import datetime, timedelta

class MaintenanceResponseService():

    def __init__(self, model, repo, actor):
        self.model = model
        self.repo = repo
        self.actor = actor

    async def get_list(self, all=False):
        sql = """
            SELECT 
                *
            FROM 
                maintenance_responses 
            """
        values = {}
        if all:
            has_permissions(self.actor.permissions, 'MANAGE_MAINTENANCE_RESPONSE', 'all')
        else:
            sql += "WHERE mechanic = :mechanic"
            values["mechanic"] = self.actor.id
        sql += " ORDER BY id DESC"
        cars = await self.repo.fetch_all(sql, values)
        return cars

    async def get_maintenance_response_by_id(self, id):
        sql = """
            SELECT 
                *
            FROM 
                maintenance_responses
            WHERE 
                id = :id
            """
        values = {"id": id}
        if not has_permissions(self.actor.permissions, 'MANAGE_MAINTENANCE_RESPONSE', 'all', False):
            sql += " and mechanic = :mechanic"
            values["mechanic"] = self.actor.id
        maintenance_response = await self.repo.fetch_one(sql, values)
        if not maintenance_response:
            raise HTTPException(404, 'Maintenance response not found')
        return maintenance_response

    async def get_maintenance_response_by_request(self, request):
        sql = """
            SELECT 
                *
            FROM 
                maintenance_responses
            WHERE 
                request = :request and mechanic = :mechanic
            """
        values = {"request": request, "mechanic": self.actor.id}
        maintenance_response = await self.repo.fetch_one(sql, values)
        return maintenance_response

    async def create(self, maintenance_response: CreateMaintenanceResponse):
        # Search resposne 
        result = await self.get_maintenance_response_by_request(maintenance_response.request)
        if result:
            raise HTTPException(409, 'Maintenance response already exists')
        await self.save(maintenance_response)
        maintenance_responses = await self.get_list()
        return maintenance_responses[0].id

    async def save(self, maintenance_response):
        sql = """INSERT INTO maintenance_responses (status, request, price, message, proposed_date, mechanic, created_at) 
        VALUES(:status, :request, :price, :message, :proposed_date, :mechanic, :created_at)"""

        values = {
            "status": maintenance_response.status,
            "request": maintenance_response.request,
            "price": maintenance_response.price,
            "message": maintenance_response.message,
            "proposed_date": maintenance_response.proposed_date,
            "created_at": datetime.today(),
            "mechanic": self.actor.id
        }
        return await self.repo.execute(sql, values)

    async def update_response(self, maintenance_response: UpdateMaintenanceResponse):
        
        # Search response 
        await self.get_maintenance_response_by_id(maintenance_response.id)

        # Update
        await self.update(maintenance_response)

    async def update(self, maintenance_response):
        sql = """UPDATE maintenance_responses set status = :status, request = :request,
        price = :price, message = :message, proposed_date = :proposed_date, mechanic = :mechanic 
        WHERE id = :id and mechanic = :mechanic"""
        values = {
            "id": maintenance_response.id,
            "status": maintenance_response.status,
            "request": maintenance_response.request,
            "price": maintenance_response.price,
            "message": maintenance_response.message,
            "proposed_date": maintenance_response.proposed_date,
            "mechanic": self.actor.id
        }
        return await self.repo.execute(sql, values)

    async def delete(self, id):
        sql = """DELETE FROM maintenance_responses WHERE id = :id AND mechanic = :mechanic"""
        values = {
            "id": id,
            "mechanic": self.actor.id
        }
        return await self.repo.execute(sql, values)

"""Maintenance Request Service."""
from fastapi import HTTPException
from schemas.request.maintenance_request import CreateMaintenanceRequest, UpdateMaintenanceRequest
from services.car import CarService
from services.mechanic import MechanicService
from utils.auth import has_permissions
from datetime import datetime, timedelta

class MaintenanceRequestService():

    def __init__(self, model, repo, actor):
        self.model = model
        self.repo = repo
        self.actor = actor

    async def get_list_by_status(self, status):
        sql = """
            SELECT 
                mrq.*, mrs.status
            FROM 
                maintenance_requests mrq
            LEFT JOIN
                maintenance_responses mrs ON mrq.id = mrs.request
            """
        values = {}
        sql += "WHERE mrq.mechanic = :mechanic OR mrq.mechanic is null"
        values["mechanic"] = self.actor.id
        sql += " ORDER BY id DESC"
        cars = await self.repo.fetch_all(sql, values)
        return cars

    async def get_list(self, all=False):
        sql = """
            SELECT 
                *
            FROM 
                maintenance_requests 
            """
        values = {}
        if all:
            has_permissions(self.actor.permissions, 'MANAGE_MAINTENANCE_REQUEST', 'all')
        else:
            sql += "WHERE client = :client"
            values["client"] = self.actor.id
        sql += " ORDER BY id DESC"
        cars = await self.repo.fetch_all(sql, values)
        return cars

    async def get_maintenance_request_by_id(self, id):
        sql = """
            SELECT 
                *
            FROM 
                maintenance_requests
            WHERE 
                id = :id
            """
        values = {"id": id}
        if not has_permissions(self.actor.permissions, 'MANAGE_MAINTENANCE_REQUEST', 'all', False):
            sql += " and client = :client"
            values["client"] = self.actor.id
        maintenance_request = await self.repo.fetch_one(sql, values)
        if not maintenance_request:
            raise HTTPException(404, 'Maintenance request not found')
        return maintenance_request

    async def create(self, maintenance_request: CreateMaintenanceRequest):
        # Search car
        car_svc = CarService(self.model, self.repo, self.actor)
        await car_svc.get_car_by_id(maintenance_request.car)
        
        # Search mechanic
        if maintenance_request.mechanic:
            mechanic_svc = MechanicService(self.model, self.repo)
            await mechanic_svc.get_mechanic_by_id(maintenance_request.mechanic)

        # Save
        await self.save(maintenance_request)
        maintenance_requests = await self.get_list()
        return maintenance_requests[0].id

    async def save(self, maintenance_request):
        sql = """INSERT INTO maintenance_requests (car, services, description, client, mechanic, expires_at, created_at) 
        VALUES(:car, :services, :description, :client, :mechanic, :expires_at, :created_at)"""

        values = {
            "car": maintenance_request.car,
            "services": str(maintenance_request.services),
            "description": maintenance_request.description,
            "client": self.actor.id,
            "mechanic": maintenance_request.mechanic,
            "expires_at": datetime.today() + timedelta(2),
            "created_at": datetime.today()
        }
        return await self.repo.execute(sql, values)

    async def update_request(self, maintenance_request: UpdateMaintenanceRequest):
        
        # Search request
        await self.get_maintenance_request_by_id(maintenance_request.id)

        # Search car
        car_svc = CarService(self.model, self.repo, self.actor)
        await car_svc.get_car_by_id(maintenance_request.car)
        
        # Search mechanic
        if maintenance_request.mechanic:
            mechanic_svc = MechanicService(self.model, self.repo)
            await mechanic_svc.get_mechanic_by_id(maintenance_request.mechanic)

        # Update
        await self.update(maintenance_request)

    async def update(self, maintenance_request):
        sql = """UPDATE maintenance_requests set car = :car, services = :services,
        description = :description, mechanic = :mechanic WHERE id = :id and client = :client"""
        values = {
            "id": maintenance_request.id,
            "car": maintenance_request.car,
            "services": str(maintenance_request.services),
            "description": maintenance_request.description,
            "client": self.actor.id,
            "mechanic": maintenance_request.mechanic
        }
        return await self.repo.execute(sql, values)

    async def delete(self, id):
        sql = """DELETE FROM maintenance_requests WHERE id = :id AND client = :client"""
        values = {
            "id": id,
            "client": self.actor.id
        }
        return await self.repo.execute(sql, values)

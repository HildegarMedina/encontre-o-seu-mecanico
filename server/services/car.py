"""Car Service."""
from fastapi import HTTPException
from schemas.request.car import AddCar, UpdateCar
from utils.auth import has_permissions

class CarService():

    def __init__(self, model, repo, actor):
        self.model = model
        self.repo = repo
        self.actor = actor

    async def get_list(self, all=False):
        sql = """
            SELECT 
                *
            FROM 
                cars 
            """
        values = {}
        if all:
            has_permissions(self.actor.permissions, 'MANAGE_CARS', 'all')
        else:
            sql += "WHERE client = :client"
            values["client"] = self.actor.id
        cars = await self.repo.fetch_all(sql, values)
        return cars

    async def get_car_by_id(self, id):
        sql = """
            SELECT 
                *
            FROM 
                cars 
            WHERE 
                id = :id
            """
        values = {"id": id}
        if not has_permissions(self.actor.permissions, 'MANAGE_CARS', 'all', False):
            sql += " and client = :client"
            values["client"] = self.actor.id
        car = await self.repo.fetch_one(sql, values)
        if not car:
            raise HTTPException(404, 'Car not found')
        return car

    async def get_car_by_details(self, brand, model, version, year, client):
        sql = """
            SELECT 
                *
            FROM 
                cars 
            WHERE 
                brand = :brand and model = :model and version = :version
                and year = :year and client = :client"""
        values = {
            "brand": brand,
            "model": model,
            "version": version,
            "year": year,
            "client": client,
        }
        car = await self.repo.fetch_one(sql, values)
        if car:
            car = dict(car)
        return car

    async def add(self, car: AddCar):
        find_car = await self.get_car_by_details(car.brand, car.model, car.version, car.year, self.actor.id)
        if not find_car:
            await self.save(car)
            car = await self.get_car_by_details(car.brand, car.model, car.version, car.year, self.actor.id)
            return car["id"]
        raise HTTPException(409, "Car already registered")

    async def change_details(self, car: UpdateCar):
        find_car = await self.get_car_by_details(car.brand, car.model, car.version, car.year, self.actor.id)
        if not find_car:
            return await self.update(car)
        raise HTTPException(409, "Car already registered")

    async def save(self, car):
        sql = """INSERT INTO cars (brand, model, version, year, client) 
        VALUES(:brand, :model, :version, :year, :client)"""
        values = {
            "brand": car.brand,
            "model": car.model,
            "version": car.version,
            "year": car.year,
            "client": self.actor.id
        }
        return await self.repo.execute(sql, values)

    async def update(self, car):
        sql = """UPDATE cars set brand = :brand, model = :model, version = :version, year = :year 
        WHERE id = :id and client = :client"""
        values = {
            "id": car.id,
            "brand": car.brand,
            "model": car.model,
            "version": car.version,
            "year": car.year,
            "client": self.actor.id
        }
        return await self.repo.execute(sql, values)

    async def delete(self, id):
        sql = """DELETE FROM cars WHERE id = :id AND client = :client"""
        values = {
            "id": id,
            "client": self.actor.id
        }
        return await self.repo.execute(sql, values)

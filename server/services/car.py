"""Car Service."""
from datetime import datetime
from fastapi import HTTPException
from schemas.request.car import AddCar, UpdateCar
import json

class CarService():

    def __init__(self, model, repo, client):
        self.model = model
        self.repo = repo
        self.client = client

    async def get_list(self):
        sql = """
            SELECT 
                *
            FROM 
                cars 
            WHERE 
                client = :client"""
        values = {
            "client": self.client.id,
        }
        cars = await self.repo.fetch_all(sql, values)
        return cars

    async def get_car_by_id(self, id):
        sql = """
            SELECT 
                *
            FROM 
                cars 
            WHERE 
                client = :client and id = :id"""
        values = {
            "client": self.client.id,
            "id": id,
        }
        cars = await self.repo.fetch_one(sql, values)
        return cars

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
        find_car = await self.get_car_by_details(car.brand, car.model, car.version, car.year, self.client.id)
        if not find_car:
            await self.save(car)
            car = await self.get_car_by_details(car.brand, car.model, car.version, car.year, self.client.id)
            return car["id"]
        raise HTTPException(409, "Car already registered")

    async def change_details(self, car: UpdateCar):
        find_car = await self.get_car_by_details(car.brand, car.model, car.version, car.year, self.client.id)
        if not find_car:
            await self.update(car)
            car = await self.get_car_by_details(car.brand, car.model, car.version, car.year, self.client.id)
            return car["id"]
        raise HTTPException(409, "Car already registered")

    async def save(self, car):
        sql = """INSERT INTO cars (brand, model, version, year, client) 
        VALUES(:brand, :model, :version, :year, :client)"""
        values = {
            "brand": car.brand,
            "model": car.model,
            "version": car.version,
            "year": car.year,
            "client": self.client.id
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
            "client": self.client.id
        }
        return await self.repo.execute(sql, values)

    async def delete(self, id):
        sql = """DELETE FROM cars WHERE id = :id AND client = :client"""
        values = {
            "id": id,
            "client": self.client.id
        }
        return await self.repo.execute(sql, values)

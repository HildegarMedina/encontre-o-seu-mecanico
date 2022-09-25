"""Seed script."""
import sys
import asyncio
from datetime import datetime
import os

sys.path.append("..")

from repository.sql import Repository
from database.db import db
from domain import model

# Profiles seed
profiles_seed = [
    {
        "id": 1,
        "name": 'admin',
        "description": "Administrador del sitio",
        "permissions": '{"MANAGE_CLIENT": true, "MANAGE_MECHANICS": true, "MANAGE_PROFILES": true, "MANAGE_SERVICES": true, "MAINTENANCE_REQUEST": true, "MAINTENANCE_RESPONSE": true, "MANAGE_CARS": true, "MECHANICAL_RATING": true, "CLIENT_RATING": true}',
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "name": 'client',
        "description": "Cliente",
        "permissions": '{"MANAGE_CLIENT": false, "MANAGE_MECHANICS": false, "MANAGE_PROFILES": false, "MANAGE_SERVICES": false, "MAINTENANCE_REQUEST": true, "MAINTENANCE_RESPONSE": false, "MANAGE_CARS": true, "MECHANICAL_RATING": true, "CLIENT_RATING": false}',
        "created_at": datetime.now()
    },
    {
        "id": 3,
        "name": 'mechanic',
        "description": "Mecánico",
        "permissions": '{"MANAGE_CLIENT": false, "MANAGE_MECHANICS": false, "MANAGE_PROFILES": false, "MANAGE_SERVICES": false, "MAINTENANCE_REQUEST": false, "MAINTENANCE_RESPONSE": true, "MANAGE_CARS": false, "MECHANICAL_RATING": false, "CLIENT_RATING": true}',
        "created_at": datetime.now()
    }
]

async def profiles(repo):
    sql = """INSERT INTO profiles (id, name, description, permissions, created_at) 
    VALUES(:id, :name, :description, :permissions, :created_at)"""
    await repo.execute_many(sql, profiles_seed)
    if not os.environ.get("RUNNING_TESTS"):
        print(f"{len(profiles_seed)} profiles added")

async def seed(repo):
    
    # Truncate
    await repo.execute(query=f"TRUNCATE ONLY {', '.join(model.tables)};")

    # Seed profiles
    await profiles(repo)

async def run():
    
    # Connect
    await db.connect()

    # Repo
    repo = Repository(db)

    # Seed
    await seed(repo)

    # Disconnect
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(run())

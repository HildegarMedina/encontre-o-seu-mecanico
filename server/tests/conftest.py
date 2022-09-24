"""Pytest setup."""
from app import app
from repository.sql import Repository
from database.db import db
import asyncio
import pytest
import pytest_asyncio
from domain import model
from scripts import seed
from async_asgi_testclient import TestClient

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="module")
async def setup():
    await db.connect()
    repo = Repository(db)
    await repo.execute(query=f"TRUNCATE ONLY {', '.join(model.tables)};")
    await seed.profiles(repo)
    async with TestClient(app) as client:
        yield repo, client
    await db.disconnect()


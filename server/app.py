from fastapi import FastAPI
from routers import auth
from database.db import db

# App
app = FastAPI()

# Routers
app.include_router(auth.router)

# Events
@app.on_event("startup")
async def startup_event():
    """Connect database."""
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """App shutdown event."""
    await db.disconnect()

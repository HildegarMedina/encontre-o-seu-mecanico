from fastapi import FastAPI
from routers import client, auth, mechanic, car, maintenance_request
from database.db import db

# App
app = FastAPI(
    title="Encontre o seu Mecánico",
    description='API do site encontre o seu mecanico',
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Routers
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(mechanic.router)
app.include_router(car.router)
app.include_router(maintenance_request.router)

# Events
@app.on_event("startup")
async def startup_event():
    """Connect database."""
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """App shutdown event."""
    await db.disconnect()

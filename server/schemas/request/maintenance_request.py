from typing import Optional
from pydantic import BaseModel

class CreateMaintenanceRequest(BaseModel):
    car: int
    services: list[str]
    description: str
    mechanic: Optional[int]

class UpdateMaintenanceRequest(CreateMaintenanceRequest):
    id: int
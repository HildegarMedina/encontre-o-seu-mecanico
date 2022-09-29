from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel
from config.config import STATUS_MAINTENANCE_RESPONSE_ALLOWED

class CreateMaintenanceResponse(BaseModel):
    status: Literal[STATUS_MAINTENANCE_RESPONSE_ALLOWED]
    request: int
    price: float
    message: str
    proposed_date: datetime

class UpdateMaintenanceResponse(CreateMaintenanceResponse):
    id: int
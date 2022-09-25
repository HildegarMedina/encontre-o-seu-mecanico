from pydantic import BaseModel

class AddCar(BaseModel):
    """AddCar model."""
    brand: str
    model: str
    version: str
    year: int

class UpdateCar(AddCar):
    id: int
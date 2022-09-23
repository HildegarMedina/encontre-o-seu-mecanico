from pydantic import BaseModel

class CreateClient(BaseModel):
    """CreateClient model."""
    full_name: str
    email: str
    password: str
    zip_code: int
    country: str
    state: str
    city: str
    address: str
    complement: str
    phone: str
    identification: str

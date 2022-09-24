from pydantic import BaseModel

class CreateMechanic(BaseModel):
    """CreateMechanic model."""
    company_logo: str
    company_name: str
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
    services: list[str]

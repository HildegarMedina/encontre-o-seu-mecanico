from pydantic import BaseModel
from typing import Optional, Union

class AccessTokenResponse(BaseModel):
    id: int
    company_logo: Optional[str]
    company_name: Optional[str]
    full_name: str
    email: str
    zip_code: int
    country: str
    state: str
    city: str
    address: str
    complement: str
    phone: str
    identification: str
    profile: Union[str, None]
    permissions: str
    services: Optional[list[str]]
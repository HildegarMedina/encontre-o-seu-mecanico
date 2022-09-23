from pydantic import BaseModel
from typing import Union


class ClientAccessTokenResponse(BaseModel):
    id: int
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
    profile: Union[int, None]
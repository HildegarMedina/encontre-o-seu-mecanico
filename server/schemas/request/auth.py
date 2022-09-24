from pydantic import BaseModel, validator
from fastapi import HTTPException

class Authentication(BaseModel):
    """Authentication model."""
    email: str
    password: str
    type: str

class Authenticated(BaseModel):
    Authorization: str

    @validator('Authorization')
    def validateAuthorization(cls, v):
        # Validando formato Bearer ('Bearer <token>')
        v_split = v.split(' ')
        if len(v_split) < 2 or v_split[0] != 'Bearer':
            raise HTTPException(401, "Invalid token")
        token = v_split[1]
        # Validando formato JWT (header.body.signature)
        token_split = token.split('.')
        if len(token_split) < 3:
            raise HTTPException(401, "Invalid token")
        return token
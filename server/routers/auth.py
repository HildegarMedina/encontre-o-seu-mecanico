from fastapi import APIRouter, Header
from domain import model
from schemas.request.auth import Authentication
from schemas.response.auth import AccessTokenResponse
from services.auth import AuthService
from database.db import db
from repository.sql import Repository
from utils.auth import get_user_auth

repo = Repository(db)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/me", response_model=AccessTokenResponse)
async def me(type: str = 'client', Authorization: str = Header(...)):
    return await get_user_auth(Authorization, type)

@router.post('')
async def authentication(auth: Authentication):
    """Authenticate a user."""
    auth_svc = AuthService(model, repo)
    return await auth_svc.authenticate(auth.email, auth.password, auth.type)

from fastapi import APIRouter, Header
from domain import model
from schemas.request.auth import Authentication
from services.auth import AuthService
from database.db import db
from repository.sql import Repository
from utils.auth import get_user_auth

repo = Repository(db)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/me")
async def me(Authorization: str = Header(...)):
    return await get_user_auth(Authorization)

@router.post('/client')
async def authentication_client(auth: Authentication):
    """Authenticate a user."""
    auth_svc = AuthService(model, repo)
    return await auth_svc.authenticate(auth.email, auth.password)
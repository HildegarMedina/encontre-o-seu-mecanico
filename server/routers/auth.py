from fastapi import APIRouter, Header
from database.db import db
from repository.sql import Repository

repo = Repository(db)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/me")
async def me():
    return "ME"

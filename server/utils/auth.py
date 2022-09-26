from passlib.context import CryptContext
from fastapi import HTTPException
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_auth(Authorization, type):
    from services.auth import AuthService
    from schemas.request.auth import Authenticated
    from domain import model
    from repository.sql import Repository
    from database.db import db
    repo = Repository(db)
    auth = Authenticated(Authorization=Authorization)
    auth_svc = AuthService(model, repo)
    user = auth_svc.me(auth.Authorization, type)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def has_permissions(permissions, permission, expected=None, raiseException=True):
    permissions = json.loads(permissions)
    if ((permissions[permission] != expected and expected) or not permissions[permission]):
        if not raiseException:
            return False
        else:
            raise HTTPException(401, 'You do not have permissions to ' + permission.lower().replace('_', ' '))
    return True
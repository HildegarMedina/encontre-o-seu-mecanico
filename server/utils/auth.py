from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_auth(Authorization):
    from services.auth import AuthService
    from schemas.request.auth import Authenticated
    from domain import model
    from repository.sql import Repository
    from database.db import db
    repo = Repository(db)
    auth = Authenticated(Authorization=Authorization)
    auth_svc = AuthService(model, repo)
    user = auth_svc.me(auth.Authorization)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
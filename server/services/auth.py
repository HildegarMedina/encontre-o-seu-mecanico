"""Auth Service."""
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, HTTPException, status
from services.client import ClientService
from services.mechanic import MechanicService
from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas.response.auth import AccessTokenResponse
from utils.auth import verify_password

class AuthService():

    def __init__(self, model, repo):
        self.model = model
        self.repo = repo

    def create_access_token(self, user, type='client'):
        to_encode = dict(AccessTokenResponse(**user))
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": int(expire.timestamp())})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {
            "access_token": encoded_jwt
        }

    async def authenticate(self, email, password, type):
        if type == "client":
            user_svc = ClientService(self.model, self.repo)
            user = await user_svc.get_client_by_email(email)
        elif type == "mechanic":
            mechanic_svc = MechanicService(self.model, self.repo)
            user = await mechanic_svc.get_mechanic_by_email(email)
        if user:
            if verify_password(password, user["password"]):
                return self.create_access_token(user, type)
        raise HTTPException(401, "Wrong email or password")
    
    async def me(self, Authorization: str, type='client'):
        Authorization = Authorization.replace("Bearer ", "")
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(Authorization, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            profile: str = payload.get("profile")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = None
        if type == 'client' and profile == "client":
            user_svc = ClientService(self.model, self.repo)
            user = await user_svc.get_client_by_email(email)
        elif type == 'mechanic' and profile == "mechanic":
            mechanic_svc = MechanicService(self.model, self.repo)
            user = await mechanic_svc.get_mechanic_by_email(email)
        if user is None:
            raise credentials_exception
        return AccessTokenResponse(**user)

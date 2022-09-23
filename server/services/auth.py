"""Auth Service."""
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, HTTPException, status
from services.client import ClientService
from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas.response.auth import ClientAccessTokenResponse
from utils.auth import verify_password

class AuthService():

    def __init__(self, model, repo):
        self.model = model
        self.repo = repo

    def create_access_token(self, user, type='client'):
        if type == 'client':
            to_encode = dict(ClientAccessTokenResponse(**user))
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": int(expire.timestamp())})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {
            "access_token": encoded_jwt
        }

    async def authenticate(self, email, password, type='client'):
        if type == "client":
            user_svc = ClientService(self.model, self.repo)
            user = await user_svc.get_client_by_email(email)
        if user:
            if verify_password(password, user.password):
                return self.create_access_token(user, type)
        raise HTTPException(401, "Wrong email or password")
    
    async def me(self, Authorization: str):
        Authorization = Authorization.replace("Bearer ", "")
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(Authorization, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user_svc = ClientService(self.model, self.repo)
        user = await user_svc.get_client_by_email(email)
        if user is None:
            raise credentials_exception
        return ClientAccessTokenResponse(**user)
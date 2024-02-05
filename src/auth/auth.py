from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import status, APIRouter

from config import JWT_SECRET_KEY
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt

from src.auth.token_schemas import TokenData, Token
from src.dependencies.dependencies import user_service
from src.models import User
from src.servises.users import UserService

ACCESS_TOKEN_EXPIRE_MINUTES = 30

ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", scheme_name="JWT")

auth_router = APIRouter(prefix='')


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(
        username: str,
        password: str,
        user_serv: Annotated[UserService, Depends(user_service)]
):
    user = await user_serv.get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_serv: Annotated[UserService, Depends(user_service)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception:
        raise credentials_exception
    user = await user_serv.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@auth_router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_serv: Annotated[UserService, Depends(user_service)]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, user_serv)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

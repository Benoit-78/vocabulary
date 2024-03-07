"""
    Creator:
        B.Delorme
    Creation date:
        5th March 2024
    Main purpose:
        Provide a secure way to handle users secrets.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "5ab141bc521af95eb0723018e87384ca6a3a1548f803737b23ddc30cf2576d06"
ALGORITHM = "HS256"  # used to sign the JWT token
ACCESS_TOKEN_EXPIRE_MINUTES = 30

sample_app = FastAPI()
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    username: str | None = None



class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None



class UserInDB(User):
    hashed_password: str



def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(users_db, username: str):
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_users_db, username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


def fake_decode_token(token):
    """
    This doesn't provide any security at all. Check the next version
    """
    user = get_user(fake_users_db, token)
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
    ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Update get_current_user to receive the same token as before, but this time, using JWT tokens.
    Decode the received token, verify it, and return the current user.
    If the token is invalid, return an HTTP error right away.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise credentials_exception from exc
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
    ):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@sample_app.get("/")
async def root():
    return {"message": "Hello World"}


@sample_app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> Token:
    """
    Create a timedelta with the expiration time of the token.
    Create a real JWT access token and return it.
    """
    user = authenticate_user(
        fake_users_db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@sample_app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
    ):
    return current_user


@sample_app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
    ):
    return [{"item_id": "Foo", "owner": current_user.username}]

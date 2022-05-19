from datetime import datetime, timedelta
from typing import List, Optional, Union

from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SCOPES = ["job", "client", "note"]


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    user_id: str
    scopes: Optional[List[str]]


class TokenData(BaseModel):
    username: Union[str, None] = None


def create_access_token(user_id: str):
    expires_delta = timedelta(minutes=90)

    data = {"sub": user_id, "scopes": SCOPES}

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        scopes = payload.get("scopes")
        if user_id is None:
            raise credentials_exception
        user = User(
            user_id=user_id,
            scopes=scopes
        )

    except JWTError:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not any(elem in SCOPES for elem in current_user.scopes):
        raise HTTPException(status_code=400, detail="Scope insufficient")
    return current_user.user_id

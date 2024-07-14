from jose import JWTError, jwt
import secrets
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Set up the token creation scheme using bearer
token_creation_scheme = OAuth2PasswordBearer(tokenUrl='login')

# random secret key and set algorithm and token expiration time
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# to create a JWT token


def create_token(data: dict):
    to_be_encoded = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_be_encoded.update({"exp": expire})
    encoded_jwt = jwt.encode(to_be_encoded, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the access tokan


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))  # Ensure id is a string
    except JWTError:
        raise credentials_exception

    return token_data

# Dependency to get the current user based on the token

def get_current_user(token: str = Depends(token_creation_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exception)

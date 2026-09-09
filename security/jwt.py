from datetime import (
  datetime, 
  timezone, 
  timedelta)
from typing import Annotated

from fastapi import (
  Depends, 
  HTTPException)
from fastapi.security import OAuth2PasswordBearer

from jose import (
  JWTError, 
  jwt)

from pydantic import BaseModel
from models.user import User

from routers.auth import db_dependency


JWT_SECRET_KEY = "8331cde2c4c9fb46b17e12e4350016fc919ae50556e28e1d77d565939c84f602"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 100

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class TokenResponse(BaseModel):
  access_token: str 
  token_type: str

def create_access_token(user_id: int): 
  expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  payload = {
    "sub": str(user_id),
    "exp": expires
  }

  return jwt.encode(
    payload, 
    JWT_SECRET_KEY,
    algorithm=JWT_ALGORITHM
  )

def decode_access_token(token: str):
  try: 
    payload = jwt.decode(
      token,
      JWT_SECRET_KEY,
      algorithms=[JWT_ALGORITHM]
    )

    user_id = payload["sub"]

    if user_id is None: 
      return None 
      
    return user_id 

  except JWTError:
    return None 

def get_current_user(
  token: Annotated[str, Depends(oauth2_scheme)],
  db: db_dependency
  ):

  try:
    payload = jwt.decode(
      token,
      JWT_SECRET_KEY,
      algorithms=[JWT_ALGORITHM]
    )

    user_id = int(payload["sub"])
    
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
      raise HTTPException(
        status_code=401,
        detail="User is not found."
      )

  except JWTError:
    raise HTTPException(
      status_code=401,
      detail="Token is invalid or expired."
    )
  
  return user
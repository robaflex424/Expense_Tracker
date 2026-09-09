from typing import Annotated

from sqlalchemy import or_

from security.hashing import hash_password, verify_password
from sqlalchemy.orm import Session
from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import (
  UserCreate, 
  UserLogin,
  UserResponse)
from security.jwt import (
  TokenResponse,
  create_access_token, 
  decode_access_token)
from models.user import User

router = APIRouter(
  prefix="/auth",
  tags=["auth"]
)

db_dependency = Annotated(Session, Depends(get_db))

@router.post("/register", response_model=UserResponse ,status_code=201)
async def register_user(
  db: db_dependency, 
  user_create: UserCreate
  ):

  existing_user = db.query(User).filter(
    or_(
      User.email == user_create.email, 
      User.username == user_create.username
    )
  ).first()

  hashed_pass = hash_password(user_create.password)

  if existing_user is not None:
    raise HTTPException(
      status_code=409,
      detail="User or Email already exists"
    )
  
  user_model = User(
    username = user_create.username,
    email = user_create.email,
    hashed_password = hashed_pass
  )  
  
  db.add(user_model)
  db.commit()
  db.refresh(user_model)

  return user_model

@router.post("/login", response_model=TokenResponse, status_code=200)
async def login_user(
    db: db_dependency,
    user_login: UserLogin
  ):

  user_model = db.query(User).filter(
    User.username == user_login.username
  ).first()

  if user_model is None:
    raise HTTPException(
      status_code=404,
      detail="Account doesn't exist"
    )
  
  if verify_password(
    user_login.password, 
    user_model.hashed_password
  ) is False:
    raise HTTPException(
      status_code=401,
      detail="Incorrect Credentials"
    )
  
  access_token = create_access_token(user_model.id)

  return {
    "access_token": access_token,
    "token_type": "Bearer"
  }

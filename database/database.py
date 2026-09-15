from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_SQLITE_DATABASE_URL = "sqlite:///./expense_tracker.db"

engine = create_engine(
  SQLALCHEMY_SQLITE_DATABASE_URL,
  connect_args={
    "check_same_thread": False
  }
)

LocalSession = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

def get_db():
  db = LocalSession()
  try: 
    yield db 
  finally: 
    db.close() 

db_dependency = Annotated[Session, Depends(get_db)]

Base = declarative_base()
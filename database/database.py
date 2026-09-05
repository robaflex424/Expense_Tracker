from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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

Base = declarative_base()
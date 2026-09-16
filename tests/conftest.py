import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.database import Base, get_db

from main import app

SQLALCHEMY_SQLITE_TESTING_DATABASE = "sqlite:///./test_expense_tracker.db"

engine = create_engine(
  SQLALCHEMY_SQLITE_TESTING_DATABASE,
  connect_args={
    "check_same_thread": False
  },
  poolclass=StaticPool
)

TestingLocalSession = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

@pytest.fixture
def db():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)

  db = TestingLocalSession() 

  try: 
    yield db 
  finally: 
    db.close()

@pytest.fixture
def client(db):
  def override_get_db():
    yield db 
  
  app.dependency_overrides[get_db] = override_get_db

  with TestClient(app) as client: 
    yield client 
  
  app.dependency_overrides.clear()
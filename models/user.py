from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from database.database import Base 

class User(Base): 
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(50), unique=True, nullable=False)
  email = Column(String(50), unique=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
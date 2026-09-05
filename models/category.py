from datetime import datetime, timezone 
from database.database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime

class Category(Base):
  __tablename__ = "categories"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(50), nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) )
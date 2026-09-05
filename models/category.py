from datetime import datetime, timezone

from sqlalchemy.orm import relationship 
from database.database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, UniqueConstraint

class Category(Base):
  __tablename__ = "categories"
  __table_args__ = (
    UniqueConstraint("user_id", "name", name="unique_user_category"),
  )

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(50), nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="categories")
  transactions = relationship("Transaction", back_populates="category")
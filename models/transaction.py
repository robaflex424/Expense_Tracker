from datetime import datetime, timezone
from sqlalchemy import Column, ForeignKey, DateTime, Integer, Numeric, String
from sqlalchemy.orm import relationship
from database.database import Base

class Transaction(Base):
  __tablename__ = "transactions"

  id = Column(Integer, primary_key=True, index=True)
  amount = Column(Numeric(10, 2), nullable=False)
  description = Column(String(300))
  type = Column(String, nullable=False)
  category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  transaction_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="transactionsuser")
  category = relationship("Category", back_populates="transactions")
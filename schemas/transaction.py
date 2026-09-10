from datetime import datetime 
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

class TransactionCreate(BaseModel):
  amount: Decimal = Field(gt=0)
  description: str
  type: Literal["income", "expense"]
  category_id: int = Field(gt=0)
  transaction_date: datetime

class TransactionResponse(BaseModel):
  id: int
  amount: int 
  description: str 
  type: str 
  category_id: int 
  user_id: int 
  transaction_date: datetime 
  created_at: datetime 

  model_config = ConfigDict(from_attributes=True)
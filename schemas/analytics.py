from decimal import Decimal
from pydantic import BaseModel

class AnalyticsGlobalResponse(BaseModel):
  total_income: Decimal | None = None
  total_expense: Decimal | None = None
  balance: Decimal 
  transaction_count: int 
  average_transaction: Decimal 
  largest_income: Decimal | None 
  largest_expense: Decimal | None

class AnalyticsIncomeResponse(BaseModel):
  total_income: Decimal | None = None
  balance: Decimal 
  average_transaction: Decimal
  transaction_count: int

class AnalyticsExpenseResponse(BaseModel):
  total_expense: Decimal | None = None
  balance: Decimal 
  average_transaction: Decimal
  transaction_count: int

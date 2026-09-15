from fastapi import (
  APIRouter, 
  status, 
  Depends)
from decimal import Decimal
from models.transaction import Transaction
from sqlalchemy import func, select
from routers.auth import db_dependency
from models.user import User
from schemas.analytics import (
  AnalyticsGlobalResponse, 
  AnalyticsIncomeResponse, 
  AnalyticsExpenseResponse)
from security.jwt import get_current_user

router = APIRouter(
  prefix="/analytics",
  tags=["analytics"]
)

@router.get("/income", status_code=status.HTTP_200_OK, response_model=AnalyticsIncomeResponse)
async def get_income_analytics(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):

  total_income = db.query(
    func.sum(Transaction.amount)
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "income"
    ).scalar()
  
  return {"total_income": total_income}


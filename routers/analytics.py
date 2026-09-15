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

analytics_router = APIRouter(
  prefix="/analytics",
  tags=["analytics"]
)

@analytics_router.get("/income", status_code=status.HTTP_200_OK, response_model=AnalyticsIncomeResponse)
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

@analytics_router.get("/expense", status_code=status.HTTP_200_OK, response_model=AnalyticsExpenseResponse)
async def get_expense_analytics(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):
  
  total_expense = db.query(
    func.sum(Transaction.amount)
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "expense"
    ).scalar()

  return {"total_expense": total_expense}

@analytics_router.get("/balance", status_code=status.HTTP_200_OK, response_model=AnalyticsGlobalResponse)
async def get_balance_analytics(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):
  
  total_income = db.query(
    func.sum(Transaction.amount)
  ).filter(
    Transaction.user_id == current_user.id,
    Transaction.type == "income"
  ).scalar()

  total_expense = db.query(
    func.sum(Transaction.amount)
  ).filter(
    Transaction.user_id == current_user.id,
    Transaction.type == "expense"
  ).scalar()

  balance = (total_income or 0) - (total_expense or 0)

  return {"balance": balance}

@analytics_router.get("/average-expense", status_code=status.HTTP_200_OK, response_model=AnalyticsExpenseResponse)
async def get_average_expense_analytics(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):

  average_expense = db.query(
    func.avg(Transaction.amount)
  ).filter(
    Transaction.user_id == current_user.id,
    Transaction.type == "expense"
  ).scalar()

  return {"average_transaction": average_expense or Decimal("0")}

@analytics_router.get("/spending-by-category", status_code=status.HTTP_200_OK)
async def get_spendings_per_category(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):

  spendings_per_category = (
    db.query(
      Transaction.category_id,
      func.sum(Transaction.amount)
    )
    .filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "expense"
    )
    .group_by(Transaction.category_id)
    .all()
  )

  return spendings_per_category
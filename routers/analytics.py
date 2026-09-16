from datetime import date
from fastapi import (
  APIRouter, 
  status, 
  Query,
  Depends)
from decimal import Decimal
from models.transaction import Transaction
from sqlalchemy import (
  func)
from routers.auth import db_dependency
from models.user import User
from schemas.analytics import (
  AnalyticsExpenseInPercentagePerCategoryResponse,
  AnalyticsGlobalResponse, 
  AnalyticsIncomeResponse, 
  AnalyticsExpenseResponse,
  AnalyticsTopCategory)
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
async def get_spendings_by_category(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):

  spendings_by_category = (
    db.query(
      Transaction.category_id,
      func.sum(Transaction.amount).label("total_spent")
    )
    .filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "expense"
    )
    .group_by(Transaction.category_id)
    .all()
  )

  return spendings_by_category

@analytics_router.get("/income-by-category", status_code=status.HTTP_200_OK, response_model=AnalyticsIncomeResponse)
async def get_income_by_category(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):
  income_by_category = (
    db.query(
      Transaction.category_id,
      func.sum(Transaction.amount).label("total_income")
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "income"
    ).group_by(
      Transaction.category_id
    ).all()
  )

  return income_by_category

@analytics_router.get("/monthly-spending", status_code=status.HTTP_200_OK, response_model=AnalyticsExpenseResponse)
async def get_monthly_spending(
  db: db_dependency, 
  current_user: User = Depends(get_current_user)
  ):
  
  monthly_spending = (
    db.query(
      func.date_trunc("month", Transaction.transaction_date).label("month"),
      func.sum(Transaction.amount).label("total_expense")
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "expense"
    ).group_by(
      func.date_trunc("month", Transaction.transaction_date)
    ).order_by(
      func.date_trunc("month", Transaction.transaction_date)
    ).all()
  )

  return monthly_spending

@analytics_router.get("/monthly-income", status_code=status.HTTP_200_OK, response_model=AnalyticsIncomeResponse)
async def get_monthly_income(
  db: db_dependency, 
  current_user: User = Depends(get_current_user)
  ):

  monthly_income = (
    db.query(
      func.date_trunc("month", Transaction.transaction_date).label("month"),
      func.sum(Transaction.amount).label("total_income")
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "income"
    ).group_by(
      func.date_trunc("month", Transaction.transaction_date)
    ).order_by(
      func.date_trunc("month", Transaction.transaction_date)
    ).all()
  )

  return monthly_income

@analytics_router.get("/date-range", status_code=status.HTTP_200_OK, response_model=AnalyticsGlobalResponse)
async def get_date_range_analytics(
  db: db_dependency,
  current_user: User = Depends(get_current_user),
  start_date: date = Query(),
  end_date: date = Query()
  ):

  total_income = (
    db.query(
      func.sum(Transaction.amount)
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "income",
      Transaction.transaction_date >= start_date,
      Transaction.transaction_date <= end_date
    ).scalar()
  )

  total_expense = (
    db.query(
      func.sum(Transaction.amount)
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "expense",
      Transaction.transaction_date >= start_date,
      Transaction.transaction_date <= end_date
    ).scalar()
  )

  total_income = total_income or Decimal("0")
  total_expense = total_expense or Decimal("0")

  balance = total_income - total_expense

  return {
    "total_income": total_income,
    "total_expense": total_expense,
    "balance": balance
  }

@analytics_router.get("/top-category", status_code=status.HTTP_200_OK, response_model=AnalyticsTopCategory)
async def get_top_category(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):
  categories_grouped_desc = (
    db.query(
      Transaction.category_id,
      func.sum(Transaction.amount).label("total_spent")
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "expense"
    ).group_by(
      Transaction.category_id
    ).order_by(
      func.sum(Transaction.amount).label("total_spent").desc()
    ).first()
  ) 

  if categories_grouped_desc is None:
    return {
      "category_id": None
    }

  category_id = int(categories_grouped_desc[0])

  return {
    "category_id": category_id
  }

@analytics_router.get(
  "/percentage-of-category", 
  status_code=status.HTTP_200_OK,
  response_model=AnalyticsExpenseInPercentagePerCategoryResponse
  )
async def get_percentage_of_category_based_on_total_expenses(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):

  total_expense = (
    db.query(
      func.sum(Transaction.amount).label("total_spent")
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "expense"
    ).scalar()
  )

  total_expense = total_expense or Decimal("0")

  if total_expense == 0:
    return [] 
  
  category_spent = (
    db.query(
      Transaction.category_id,
      func.sum(Transaction.amount).label("category_total")
    ).filter(
      Transaction.user_id == current_user.id,
      Transaction.type == "expense"
    ).group_by(
      Transaction.category_id
    ).all()
  )

  return [
    {
      "category_id": category_id,
      "total_expense": total_expense,
      "percentage": (category_total / total_expense) * 100
    }
    for category_id, category_total in category_spent
  ]
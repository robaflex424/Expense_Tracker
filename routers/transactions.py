from fastapi import APIRouter, HTTPException, status, Depends
from models.category import Category
from models.transaction import Transaction
from models.user import User
from routers.auth import db_dependency
from schemas.transaction import (
  TransactionCreate, 
  TransactionResponse)
from security.jwt import get_current_user


router = APIRouter(
  prefix="/transactions",
  tags=["transactions"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TransactionResponse)
async def create_transaction(
  db: db_dependency,
  transaction_create: TransactionCreate,
  current_user: User = Depends(get_current_user)
  ):

  category_model = db.query(Category).filter(
    Category.id == transaction_create.category_id,
    Category.user_id == current_user.id
  ).first()

  if category_model is None:
    raise HTTPException(
      status_code=404,
      detail="Category not found"
    )
  
  transaction_model = Transaction(
    amount = transaction_create.amount,
    description = transaction_create.description,
    type = transaction_create.type,
    category_id = transaction_create.category_id,
    user_id = current_user.id,
    transaction_date = transaction_create.transaction_date
  )

  db.add(transaction_model)
  db.commit()
  db.refresh(transaction_model)

  return transaction_model
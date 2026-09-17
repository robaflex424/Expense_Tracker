from typing import Literal
from decimal import Decimal
from datetime import date
from fastapi import (
  APIRouter, 
  HTTPException,
  Path, 
  status, 
  Depends, 
  Query)
from models.category import Category
from models.transaction import Transaction
from models.user import User
from routers.auth import db_dependency
from schemas.transaction import (
  TransactionCreate, 
  TransactionResponse,
  TransactionUpdate)
from security.jwt import get_current_user


transaction_router = APIRouter(
  prefix="/transactions",
  tags=["transactions"]
)

@transaction_router.post("", status_code=status.HTTP_201_CREATED, response_model=TransactionResponse)
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

@transaction_router.get("/{transaction_id}", status_code=status.HTTP_200_OK, response_model=TransactionResponse)
async def get_transaction(
  db: db_dependency,
  current_user: User = Depends(get_current_user),
  transaction_id: int = Path(ge=1)
  ):

  transaction_model = db.query(Transaction).filter(
    Transaction.id == transaction_id,
    Transaction.user_id == current_user.id
  ).first()

  if transaction_model is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Transaction doesn't exist."
    )

  return transaction_model

@transaction_router.patch("/{transaction_id}", status_code=status.HTTP_200_OK, response_model=TransactionResponse)
async def update_transaction(
  db: db_dependency,
  transaction_update: TransactionUpdate,  
  current_user: User = Depends(get_current_user),
  transaction_id: int = Path(ge=1)
  ):

  transaction_model = db.query(Transaction).filter(
    Transaction.id == transaction_id,
    Transaction.user_id == current_user.id
  ).first()

  if transaction_model is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Transaction doesn't exist."
    )
  
  update_model = transaction_update.model_dump(exclude_unset=True)

  if "category_id" in update_model:
    category = db.query(Category).filter(
      Category.id == update_model["category_id"],
      Category.user_id == current_user.id
    ).first()

    if category is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category doesn't exist."
      )
  
  for field, value in update_model.items():
    setattr(transaction_model, field, value)
  
  db.commit()
  db.refresh(transaction_model)

  return transaction_model

@transaction_router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
  db: db_dependency,
  current_user: User = Depends(get_current_user),
  transaction_id: int = Path(gt=0)
  ):
  transaction_model = db.query(Transaction).filter(
    Transaction.id == transaction_id,
    Transaction.user_id == current_user.id
  ).first()

  if transaction_model is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Transaction not found."
    )
  
  db.delete(transaction_model)
  db.commit()

@transaction_router.get("", status_code=status.HTTP_200_OK, response_model=list[TransactionResponse])
async def get_transactions(
    db: db_dependency,
    current_user: User = Depends(get_current_user),

    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),

    type: Literal["income", "expense"] | None = None,

    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,

    start_date: date | None = None,
    end_date: date | None = None,

    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc")
):
    query = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    )

    # Filter by type
    if type is not None:
        query = query.filter(
            Transaction.type == type
        )

    # Filter by amount
    if min_amount is not None:
        query = query.filter(
            Transaction.amount >= min_amount
        )

    if max_amount is not None:
        query = query.filter(
            Transaction.amount <= max_amount
        )

    # Filter by date
    if start_date is not None:
        query = query.filter(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        query = query.filter(
            Transaction.transaction_date <= end_date
        )

    # Validate sorting
    if sort_by not in ["created_at", "transaction_date", "amount"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort field."
        )

    if sort_order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort order."
        )

    # Pagination
    offset = (page - 1) * page_size

    # Sorting
    sort_column = getattr(Transaction, sort_by)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Execute query
    transactions = query.offset(offset).limit(page_size).all()

    return transactions
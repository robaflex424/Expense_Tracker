from fastapi import APIRouter, Depends, HTTPException

from models.category import Category
from models.user import User

from routers.auth import db_dependency
from schemas.category import CategoryCreate, CategoryResponse
from security.jwt import get_current_user

router = APIRouter(
  prefix="/categories",
  tags=["categories"]
)

@router.get("", response_model=CategoryResponse)
async def get_categories(
  db: db_dependency,
  current_user: User = Depends(get_current_user)
  ):

  category_model = db.query(Category).filter(
    Category.user_id == current_user.id
    ).all()

  return category_model

@router.post("", response_model=CategoryResponse)
async def create_category(
  db: db_dependency,
  create_category: CategoryCreate,
  current_user: User = Depends(get_current_user),
  ):

  category_model = Category(name = create_category.name, user_id = current_user.id)
  
  db.add(category_model)
  db.commit()
  db.refresh(category_model)

  return category_model
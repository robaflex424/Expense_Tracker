from fastapi import (
  APIRouter, 
  Depends, 
  HTTPException, 
  Path)

from models.category import Category
from models.user import User

from routers.auth import db_dependency
from schemas.category import (
  CategoryCreate, 
  CategoryResponse, 
  CategoryUpdate)
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

  name_collision = db.query(Category).filter(
    Category.name == create_category.name, 
    Category.user_id == current_user.id
    ).first()
  
  if name_collision is not None:
    raise HTTPException(
      status_code=409,
      detail="Category with this name already exists."
    )

  category_model = Category(name = create_category.name, user_id = current_user.id)
  

  db.add(category_model)
  db.commit()
  db.refresh(category_model)

  return category_model

@router.put("{category_id}", response_model=CategoryResponse)
async def update_category(
  db: db_dependency,
  update_category: CategoryUpdate,
  current_user: User = Depends(get_current_user),
  category_id: int = Path(gt=0)
  ):
  
  category_model = db.query(Category).filter(
    Category.id == category_id,
    Category.user_id == current_user.id
  ).first()

  if category_model is None:
    raise HTTPException(
      status_code=404,
      detail="Category not found."
    )
  
  category_model.name == update_category.name

  db.commit()
  db.refresh(category_model)

  return category_model


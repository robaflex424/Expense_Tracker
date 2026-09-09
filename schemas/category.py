from datetime import datetime
from pydantic import BaseModel

class CategoryCreate(BaseModel):
  name: str 

class CategoryResponse(BaseModel):
  id: int 
  name: str 
  user_id: int 
  created_at: datetime

class CategoryUpdate(BaseModel):
  name: str
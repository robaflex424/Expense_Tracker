from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel

JWT_SECRET_KEY = "8331cde2c4c9fb46b17e12e4350016fc919ae50556e28e1d77d565939c84f602"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 100

class TokenResponse(BaseModel):
  access_token: str 
  token_type: str

def create_access_token(user_id: int): 
  expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  payload = {
    "sub": str(user_id),
    "exp": expires
  }

  return jwt.encode(
    payload, 
    JWT_SECRET_KEY,
    algorithm=JWT_ALGORITHM
  )

def decode_access_token(token: str):
  try: 
    payload = jwt.decode(
      token,
      JWT_SECRET_KEY,
      algorithms=[JWT_ALGORITHM]
    )

    user_id = payload["sub"]

    if user_id is None: 
      return None 
      
    return user_id 

  except JWTError:
    return None 
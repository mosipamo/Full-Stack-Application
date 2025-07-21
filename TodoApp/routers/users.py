from fastapi import APIRouter, Depends, HTTPException
import models
from database import SessionLocal
from pydantic import BaseModel, Field
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from starlette import status
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordChangeRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_profile(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found in token")

    user_profile = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User not found")

    return user_profile

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, new_password: PasswordChangeRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found in token")

    user_profile = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not bcrypt_context.verify(new_password.password, user_profile.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    user_profile.hashed_password = bcrypt_context.hash(new_password.new_password)
    db.add(user_profile)
    db.commit()



@router.put("/change_password/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_password_for_user(db: db_dependency, user: user_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found in token")
    
    user_profile = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user_profile:
        raise HTTPException(status_code=400, detail="Incorret phone_number")
    
    user_profile.phone_number = phone_number
    db.add(user_profile)
    db.commit()

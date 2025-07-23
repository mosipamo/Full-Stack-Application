from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models import Users
from starlette import status
from passlib.context import CryptContext
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone

router = APIRouter(prefix="/auth", tags=["Authentication"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = "2290cdf1724c4a08600e00f7ef86010f3b9acd62a4f34d59da3c6bdb46a5771c"
ALGORITHM = "HS256"

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta | None = None):
    to_encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Could not validate user.")
        return {"username": username, "id": user_id, "role": role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate user.")

        
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    """Create a new user in the system. """
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True,
        phone_number = create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()
    
    return create_user_model


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_fot_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate user and return access"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return "Failed Authentication"
    
    token = create_access_token(user.username, user.id, user.role, expires_delta=timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer"}
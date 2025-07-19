from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
from starlette import status

router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest, status_code=status.HTTP_201_CREATED):
    """Create a new user in the system. """
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = create_user_request.password,  # In a real app, hash the password
        role = create_user_request.role,
        is_active = True
    )
    
    return create_user_model


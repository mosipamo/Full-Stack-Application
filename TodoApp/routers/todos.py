from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from ..models import Todos
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/todos", 
    tags=["Todos"]
)

templates = Jinja2Templates(directory="TodoApp/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    is_complete: bool


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})

    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

    except:
        return redirect_to_login()

### endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_records_in_db(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todos).filter(user.get("id") == Todos.owner_id).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(ge=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    result = db.query(Todos).filter(Todos.id == todo_id) \
                                   .filter(user.get("id") == Todos.id).first()
    if result: 
        return result
    raise HTTPException(status_code=404, detail="Todo not found!")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    result = Todos(**todo.model_dump(), owner_id=user.get("id"))

    db.add(result)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    result = db.query(Todos).filter(Todos.id == todo_id) \
                    .filter(user.get("id") == Todos.owner_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found!")
    
    result.title = todo.title
    result.description = todo.description
    result.priority = todo.priority
    result.is_complete = todo.is_complete

    db.add(result)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    result = db.query(Todos).filter(Todos.id == todo_id) \
                    .filter(user.get("id") == Todos.owner_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found!")
    db.query(Todos).filter(Todos.id == todo_id) \
                            .filter(user.get("id") == Todos.owner_id).delete()

    db.commit()
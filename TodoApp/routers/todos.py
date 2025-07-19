from fastapi import APIRouter, Depends, HTTPException, Path
import models
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    is_complete: bool = Field()


@router.get("/")
async def read_all_records_in_db(db: db_dependency, status_code=status.HTTP_200_OK):
    return db.query(models.Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(ge=0)):
    result = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if result: 
        return result
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_200_OK)
async def create_todo(db: db_dependency, todo: TodoRequest):
    result = models.Todos(**todo.model_dump())

    db.add(result)
    db.commit()

@router.put("/todo/{todo_id}")
async def update_todo(db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):
    result = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")

    print(todo.description)
    
    result.title = todo.title
    result.description = todo.description
    result.priority = todo.priority
    result.is_complete = todo.is_complete

    db.add(result)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    result = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    db.commit()
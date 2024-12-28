
from fastapi import APIRouter, Path, Depends, HTTPException
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user


router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool


@router.get("/")
async def read_all_todos(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_a_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_a_todo(user: user_dependency,  todo_request: TodoRequest, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def update_a_todo(user: user_dependency, todo_request: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in todo_request.dict().items():
        setattr(todo_model, key, value)

    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()
    return None
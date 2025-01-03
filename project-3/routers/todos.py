from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from models import Todos
from database import SessionLocal
from .auth import get_current_user
from typing import Annotated

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

# Dependências para obter a conexão com o banco e o usuário autenticado
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Modelo para requisições relacionadas a Todos
class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

# Rota para listar todos os Todos do usuário autenticado
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id == user["id"]).all()

# Rota para listar um Todo específico pelo ID
@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int = Path(gt=0), user: user_dependency = user_dependency, db: db_dependency = db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user["id"]).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

# Rota para criar um novo Todo
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo = Todos(**todo_request.model_dump(), owner_id=user["id"])
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

# Rota para atualizar um Todo existente
@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    todo_id: int = Path(gt=0),
    todo_request: TodoRequest = Depends(),
    user: user_dependency = user_dependency,
    db: db_dependency = db_dependency
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user["id"]).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete

    db.add(todo)
    db.commit()
    return {"message": "Todo updated successfully"}

# Rota para deletar um Todo existente
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(gt=0), user: user_dependency = user_dependency, db: db_dependency = db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user["id"]).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

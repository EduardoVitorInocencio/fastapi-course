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

@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency, skip: int = 0, limit: int = 10):
    if user is None or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(Todos).all()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return


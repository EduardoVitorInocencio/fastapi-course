from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import User
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get('/', status_code=status.HTTP_200_OK)    
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(User).filter(User.id == user.get('id')).first()

@router.put('/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, data: UserVerification, db: db_dependency, username: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_db = db.query(User).filter(User.username == username).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='User not found')
    if not bcrypt_context.verify(data.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid password')
    user_db.hashed_password = bcrypt_context.hash(data.new_password)
    db.commit()
    return
from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal
from .users_repository import User, UserCreate, UsersRepository

app = FastAPI()
users_repo = UsersRepository()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ReadUserResponse(BaseModel):
    id: int
    email: str
    is_active: bool


@app.get("/users/{user_id}", response_model=ReadUserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_repo.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


class UserCreateRequest(BaseModel):
    email: str
    password: str


@app.post("/users/")
def post_users(input: UserCreateRequest, db: Session = Depends(get_db)):
    users_repo.create_user(db, UserCreate(email=input.email, password=input.password))
    return Response(status_code=200)

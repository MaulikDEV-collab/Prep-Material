#i have made this in order to understand user registration, hashing passwords
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

#in order to hash passwords you need to install the library 'passlib[bcrypt]'. pip install passlib[bcrypt]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
#here scheme tells the object which algo will be used for hashing in this case its bcrypt

#path operation for creating a new user
@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    print(user.password)
    #hash the password - user.password
    hashed_password = pwd_context.hash(user.password)
    try:
        user.password = hashed_password
        
        new_user = model.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print(e)

@app.get("/user", status_code=status.HTTP_200_OK)
def get_user(db:Session = Depends(get_db)):
    users = db.query(model.User).all()
    return users

@app.get("/user/{id}", response_model=schemas.UserOut)
def get_user_byID(id: int, db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found.")
    return user




from pydantic import BaseModel, EmailStr
from typing import Optional

#this handles the direction of us sending data to user
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

#pydantic model or schema for create_post(), #this handles the direction of us sending data to user
class PostCreate(PostBase):
    pass

#pydantic model for response, this handles the direction of us sending data to user
class Post(BaseModel):
    title : str
    content : str
    published : bool

    class Config:       #When SQLAlchemy fetches data, it returns a python object, not a dictionary. By default pydantic expects a dictionary, so returning a SQLAlchemy causes error hence we use this class config and set ORM=True
        orm_mode = True

#pydanntic schema for when creating a user
class UserCreate(BaseModel):
    email : EmailStr
    password : str

#pydanntic schema for response to creating a user
class UserOut(BaseModel):
    id : int
    email : EmailStr
    class Config:       #When SQLAlchemy fetches data, it returns a python object, not a dictionary. By default pydantic expects a dictionary, so returning a SQLAlchemy causes error hence we use this class config and set ORM=True
        orm_mode = True
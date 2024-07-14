from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True # If not provide then no problem otherwise use it
    

class PostCreate(PostBase):
    pass

class Post(PostBase):  ## RESPONSE PORTION
    id :int
    created_at : datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime



class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None
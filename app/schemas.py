from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# allll schemas where we tell the frontend
# that it is the pattern which we wnat and we expect your 
# request to be in this form otherise get out
# Also we can ensure the repsonse schmes so that we can choose 
# whcih thing to show or not to the user, like passwords and etc
# mostly inherited to reduce space

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

from typing import Optional

from pydantic import BaseModel


class Register(BaseModel):
    
    username: str
    password: str
    email: str


class Login(BaseModel):
    username: str
    password: str
    

class UpdateUser(BaseModel):
    
    username: Optional[str] 
    password: Optional[str] 

    class Config:
        orm_mode = True


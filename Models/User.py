
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Roles(str ,Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    MEMBER="MEMBER"



class User(BaseModel):
    name: str
    email: str
    password: str 
    role: Roles

class Complete_user(User):
    id: str
    created_at: datetime
    


class BaseResponse(BaseModel):
    message:str
    status :int

## Api's Model
class createUserRequest(BaseModel):
    user:User

class createUserResponse(BaseResponse):
    user_id: str 
    
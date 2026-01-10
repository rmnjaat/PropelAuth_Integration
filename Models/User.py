
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Roles(str, Enum):
    OWNER = "Owner"
    ADMIN = "Admin"
    MEMBER = "Member"



class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str 
    role: Roles
    orgId:str

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

class updateUserRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Roles] = None
    orgId: Optional[str] = None

class updateUserResponse(BaseResponse):
    pass

class deleteUserResponse(BaseResponse):
    pass
    
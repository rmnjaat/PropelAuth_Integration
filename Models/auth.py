
from pydantic.main import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str


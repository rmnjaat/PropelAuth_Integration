from fastapi import Request
from propelauth_py import User

class RequestContext():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestContext, cls).__new__(cls)
        return cls._instance

    def set_user(self, request: Request , user: User):
        request.state.user = user
    
    def get_user(self, request: Request)-> User:
        return request.state.user
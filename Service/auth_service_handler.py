
from Models.auth import LoginRequest
from Service.auth_service import AuthService


class AuthServiceHandler(AuthService):
    def login(self,request: LoginRequest):
        return {"message": "Login"}

    def logout(self,request: LoginRequest):
        return {"message": "Logout"}
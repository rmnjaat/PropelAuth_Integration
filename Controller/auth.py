from fastapi import APIRouter, Depends

from Models.auth import LoginRequest
from Service.auth_service import AuthService
from main_module import get_instance

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
    
)

def get_auth_service() -> AuthService:
    return get_instance(AuthService)

@router.post("/login")
def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return service.login(request)

@router.post("/logout")
def logout(service: AuthService = Depends(get_auth_service)):
    return service.logout()

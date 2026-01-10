
from fastapi import APIRouter, Depends, Security
from Models.auth import LogoutResponse
from Service.auth_service import auth_service
from main_module import get_instance
from packages.authenticate_user import AuthenticateUser
from propelauth_py import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_auth_service() -> auth_service:
    return get_instance(auth_service)

@router.post("/logout")
def logout(
    service: auth_service = Depends(get_auth_service),
    user: User = Security(AuthenticateUser().authenticate_user)
) -> LogoutResponse:
    # Use the user_id from the authenticated user token
    return service.logout(user.user_id)


from fastapi import APIRouter, Depends
from Models.User import createUserResponse, createUserRequest, updateUserRequest, updateUserResponse, deleteUserResponse
from Service.user_managment_service import user_managment_service
from main_module import get_instance

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


def get_user_managment_service() -> user_managment_service:
    return get_instance(user_managment_service)

@router.get("/health")
def health_check():
    return {"message": "User Management Service is running"}


@router.post("/create")
def create_user(
    request: createUserRequest,
    service: user_managment_service = Depends(get_user_managment_service)
) -> createUserResponse:
    return service.create_user(request)

@router.put("/{user_id}")
def update_user(
    user_id: str,
    request: updateUserRequest,
    service: user_managment_service = Depends(get_user_managment_service)
) -> updateUserResponse:
    return service.update_user(user_id, request)

@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    service: user_managment_service = Depends(get_user_managment_service)
) -> deleteUserResponse:
    return service.delete_user(user_id)
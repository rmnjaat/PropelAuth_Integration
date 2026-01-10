from fastapi import APIRouter
from Controller.user_managment import router as user_managment_router
from Controller.auth import router as auth_router
from Controller.auth import router as auth_router

router = APIRouter()


router.include_router(
    auth_router
)

router.include_router(
    user_managment_router
)

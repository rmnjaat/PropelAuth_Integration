
from Models.auth import LogoutResponse
from Repository.auth_repository import auth_repository
from Service.auth_service import auth_service

class auth_service_handler(auth_service):
    repository: auth_repository

    def logout(self, user_id: str) -> LogoutResponse:
        return self.repository.logout(user_id)
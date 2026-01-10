
from Models.User import createUserRequest, createUserResponse, updateUserRequest, updateUserResponse, deleteUserResponse
from Repository.user_managment_repository import user_managment_repository
from Service.user_managment_service import user_managment_service


class user_managment_service_handler(user_managment_service):

    repository: user_managment_repository

    def create_user(self, request: createUserRequest) -> createUserResponse:
        return self.repository.create_user(request)

    def update_user(self, user_id: str, request: updateUserRequest) -> updateUserResponse:
        return self.repository.update_user(user_id, request)

    def delete_user(self, user_id: str) -> deleteUserResponse:
        return self.repository.delete_user(user_id)

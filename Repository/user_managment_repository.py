
from Repository.base_repository import BaseRepository
from Models.User import createUserRequest, createUserResponse, updateUserRequest, updateUserResponse, deleteUserResponse
from abc import abstractmethod

class user_managment_repository(BaseRepository):
    @abstractmethod
    def create_user(self, request: createUserRequest) -> createUserResponse:
        pass

    @abstractmethod
    def update_user(self, user_id: str, request: updateUserRequest) -> updateUserResponse:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> deleteUserResponse:
        pass
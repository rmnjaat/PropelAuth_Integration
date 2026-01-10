
from Repository.base_repository import BaseRepository
from Models.User import createUserRequest,createUserResponse
from abc import abstractmethod

class user_managment_repository(BaseRepository):
    @abstractmethod
    def create_user(self, request:createUserRequest)->createUserResponse:
        pass
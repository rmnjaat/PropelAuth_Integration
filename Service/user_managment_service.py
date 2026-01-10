
from Service.base_service import BaseService
from Models.User import createUserRequest,createUserResponse
from abc import abstractmethod

class user_managment_service(BaseService):
    @abstractmethod
    def create_user(self, request:createUserRequest)->createUserResponse:
        pass
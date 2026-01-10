
from Models.User import createUserRequest,createUserResponse
from Repository.user_managment_repository import user_managment_repository
from Service.user_managment_service import user_managment_service


class user_managment_service_handler(user_managment_service):

    repository: user_managment_repository

    def create_user(self, request:createUserRequest)->createUserResponse:
        
        return self.repository.create_user(request)

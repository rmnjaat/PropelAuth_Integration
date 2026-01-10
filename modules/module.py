from injector import Module, provider, singleton

from Repository.user_managment_repository import user_managment_repository
from Repository.user_managment_repository_handler import user_managment_repository_handler
from Service.user_managment_service import user_managment_service
from Service.user_managment_service_handler import user_managment_service_handler

class UserModule(Module):
    @provider
    @singleton
    def provide_user_managment_repository(
        self
    )->user_managment_repository:
        return user_managment_repository_handler()

    @provider
    @singleton
    def provide_user_managment_service(
        self,
        user_managment_repository: user_managment_repository
    )->user_managment_service:
        return user_managment_service_handler(
            repository=user_managment_repository
        )
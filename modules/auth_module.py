
from injector import Module, provider, singleton
from packages.auth_provider import Auth_provider
from Repository.auth_repository import auth_repository
from Repository.auth_repository_handler import auth_repository_handler
from Service.auth_service import auth_service
from Service.auth_service_handler import auth_service_handler

class AuthModule(Module):
    @provider
    @singleton
    def provide_auth_repository(
        self, auth_provider: Auth_provider
    ) -> auth_repository:
        return auth_repository_handler(auth_provider=auth_provider)

    @provider
    @singleton
    def provide_auth_service(
        self, auth_repository: auth_repository
    ) -> auth_service:
        return auth_service_handler(repository=auth_repository)
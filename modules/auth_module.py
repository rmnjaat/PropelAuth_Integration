from injector import Module, provider, singleton

from Service.auth_service import AuthService
from Service.auth_service_handler import AuthServiceHandler

class AuthModule(Module):
    @provider
    @singleton
    def provide_auth_service(
        self
    )->AuthService:
        return AuthServiceHandler()
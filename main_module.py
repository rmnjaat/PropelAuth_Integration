from injector import Injector
from modules.module import UserModule
from modules.auth_module import AuthModule

injector = Injector([UserModule, AuthModule])

def get_instance(service_type: type):
    return injector.get(service_type)

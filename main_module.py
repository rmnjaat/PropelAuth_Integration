from injector import Injector
from module import UserModule

injector = Injector([UserModule])

def get_instance(service_type: type):
    return injector.get(service_type)

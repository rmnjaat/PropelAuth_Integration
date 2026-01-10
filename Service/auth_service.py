
from abc import abstractmethod
from Service.base_service import BaseService
class AuthService(BaseService):
    @abstractmethod
    def login(self,request):
        pass

    @abstractmethod
    def logout(self,request):
        pass
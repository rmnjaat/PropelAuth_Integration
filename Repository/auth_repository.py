
from abc import abstractmethod
from Repository.base_repository import BaseRepository
from Models.auth import LogoutResponse

class auth_repository(BaseRepository):
    @abstractmethod
    def logout(self, user_id: str) -> LogoutResponse:
        pass

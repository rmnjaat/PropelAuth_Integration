
import logging
from packages.auth_provider import Auth_provider
from Models.auth import LogoutResponse
from Repository.auth_repository import auth_repository
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class auth_repository_handler(auth_repository):
    auth_provider: Auth_provider

    def logout(self, user_id: str) -> LogoutResponse:
        try:
            client = self.auth_provider.get_client()
            logger.info(f"Logging out user: {user_id}")
            
            # Invalidate all sessions for the user
            client.logout_all_user_sessions(user_id=user_id)
            
            return LogoutResponse(
                message="Logged out successfully from all sessions",
                status=200
            )
        except Exception as e:
            logger.error(f"Logout failed for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")


import os

from propelauth_py import Auth, User, init_base_auth

class Auth_provider():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Auth_provider, cls).__new__(cls)
            cls._instance.auth_url = os.getenv("AUTH_URL")
            cls._instance.auth_key = os.getenv("AUTH_KEY")
            cls._instance.auth_v2 = init_base_auth(
                cls._instance.auth_url,
                cls._instance.auth_key
            )
        return cls._instance
    
    def verify_token(self, token:str)-> User:
        return self.auth_v2.validate_access_token_and_get_user(token)
    
    def get_client(self)->Auth:
        return self.auth_v2
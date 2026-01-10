from fastapi import HTTPException, Request
from propelauth_py import User
from packages.auth_provider import Auth_provider
from packages.request_context import RequestContext


X_AUTHTOKEN = "X-AUTH-TOKEN"

class AuthenticateUser:

    def __init__(self ):
        self.auth_provider = Auth_provider()
        self.request_context = RequestContext()

    def _get_token(self,token:str)->str:
        return token.split(" ")[1]

    def authenticate_user(self, request: Request):
        auth_header = request.headers.get(X_AUTHTOKEN)

        if not auth_header:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        # try:
        user = self.auth_provider.verify_token(auth_header)
        # except Exception as e:
        #     raise HTTPException(status_code=401, detail="Unauthorized")

        self.request_context.set_user(request, user)

        return user

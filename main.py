from fastapi import Depends, FastAPI, Security
import uvicorn

from packages.authenticate_user import AuthenticateUser
from router import router


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(
    router,
    dependencies=[
        Security(
            AuthenticateUser().authenticate_user
        )
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

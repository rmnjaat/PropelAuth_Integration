from fastapi import FastAPI
import uvicorn
from Controller.user_managment import router
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(
    router
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

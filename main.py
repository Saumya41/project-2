from fastapi import FastAPI
from auth.routes import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the authentication service!"}
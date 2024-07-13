from fastapi import FastAPI
from auth.routes import router as auth_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Password Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from .schemas import UserCreate, UserLogin, UserForgotPassword, UserResetPassword
from .models import User, Token
from .utils import get_password_hash, verify_password, create_access_token
from config import MONGO_URL, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()
client = AsyncIOMotorClient(MONGO_URL)
db = client["mydatabase"]
users_collection = db["users"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup", response_model=User)
async def signup(user: UserCreate):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user.password)
    del user_dict["password"]
    await users_collection.insert_one(user_dict)
    return user_dict

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
async def forgot_password(user: UserForgotPassword):
    
    pass

@router.post("/reset-password")
async def reset_password(user: UserResetPassword):
   
    pass

@router.post("/login/google")
async def login_google(token: str):
    # Exchange the authorization code for an access token
    # Verify the access token and retrieve user information
    # Check if the user exists in the database
    # If not, create a new user
    # Generate and return a JWT token
    pass

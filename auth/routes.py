from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import timedelta
from .schemas import UserCreate, UserLogin, UserForgotPassword, UserResetPassword
from .models import User, Token
from .utils import get_password_hash, verify_password, create_access_token, create_reset_token, decode_reset_token, send_email
from config import settings

router = APIRouter()
client = AsyncIOMotorClient(settings.MONGO_URL)
db = client["mydatabase"]
users_collection = db["users"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/forgot-password")
async def forgot_password(user: UserForgotPassword, background_tasks: BackgroundTasks):
    user_data = await users_collection.find_one({"email": user.email})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist."
        )
    
    reset_token_expires = timedelta(minutes=15)
    reset_token = create_reset_token(
        data={"sub": user.email}, expires_delta=reset_token_expires
    )
    
    reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
    email_body = f"Please use the following link to reset your password: {reset_link}"
    
    background_tasks.add_task(send_email, "Password Reset Request", user.email, email_body)
    
    return {"msg": "Password reset link has been sent to your email."}

@router.post("/reset-password")
async def reset_password(user: UserResetPassword):
    try:
        token_data = decode_reset_token(user.reset_token)
        user_email = token_data.username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token."
        )
    
    new_hashed_password = get_password_hash(user.new_password)
    await users_collection.update_one(
        {"email": user_email},
        {"$set": {"hashed_password": new_hashed_password}}
    )
    
    return {"msg": "Password has been reset successfully."}

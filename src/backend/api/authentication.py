from fastapi import APIRouter, HTTPException, Depends
from src.backend.services.business_logic import register_user, login_user
from src.backend.models.models import UserLogin, UserRegister

auth_router = APIRouter()

@auth_router.post("/register")
def register(user: UserRegister):
    success = register_user(user)
    if not success:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully"}

@auth_router.post("/login")
def login(user: UserLogin):
    token = login_user(user)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": token, "token_type": "bearer"}
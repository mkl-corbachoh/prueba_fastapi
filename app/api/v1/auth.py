from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.deps.deps import get_current_user, get_db, reqires_admin
from app.models.user import User
from app.schemas import Token, UserCreate, UserResponse
import app.service.user as user_service

api_router = APIRouter()

# ============ USUARIOS ============
@api_router.post(
    "/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = user_service.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_user


@api_router.post("/login/", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = user_service.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(sub=user.email, is_admin=user.is_admin)
    return {"access_token": token, "token_type": "Bearer"}


@api_router.get("/users/me/", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@api_router.get("/admin/ping", response_model=UserResponse)
async def admin_ping(_admin=Depends(reqires_admin)):
    return {"ok": True, "role": "admin"}

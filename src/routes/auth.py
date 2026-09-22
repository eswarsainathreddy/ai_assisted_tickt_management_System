from fastapi import APIRouter, Depends, HTTPException, Body, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated, Union, Literal
from pydantic import BaseModel
from src.database import get_db
from src.models.Users import User
from src.models.Tickets import Ticket
from src.models.Threads import Thread
from src.utils.hashing import hash_password, verify_password
from src.utils.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class RegisterRequest(BaseModel):
    username: str
    password: str
    fullname: str
    email: str
    mobile_number: str | None = None

@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):
    clean_username = payload.username.strip()
    clean_email = payload.email.strip().lower()

    if not clean_username or not payload.password:
        raise HTTPException(
            status_code=400,
            detail="Username and password are required."
        )

    if len(payload.password) < 4:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 4 characters long."
        )

    # Check if username exists
    existing_user = db.query(User).filter(User.username == clean_username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken. Please choose another username."
        )

    # Check if email exists
    existing_email = db.query(User).filter(User.email == clean_email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists."
        )

    # Generate next user_id
    user_count = db.query(User).count() + 1
    user_id = f"USR{user_count:03d}"
    while db.query(User).filter(User.user_id == user_id).first():
        user_count += 1
        user_id = f"USR{user_count:03d}"

    new_user = User(
        user_id=user_id,
        username=clean_username,
        fullname=payload.fullname.strip() or clean_username,
        email=clean_email,
        password_hash=hash_password(payload.password),
        mobile_number=payload.mobile_number
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

    token = create_access_token(
        {
            "sub": new_user.username
        }
    )

    return {
        "status": "success",
        "message": "Account created successfully",
        "access_token": token,
        "token_type": "bearer",
        "user_id": new_user.user_id,
        "username": new_user.username,
        "fullname": new_user.fullname
    }

@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "sub": user.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
        "fullname": user.fullname
    }




from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter(tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db), response: Response = None):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, 
        samesite="Lax", 
        secure=True 
    )
    
    return {"access_token": access_token}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from app.model.user import User, hash_password
from app.database import get_db
from app.schema.user import UserCreate, UserLogin

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@auth_router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if existing_user:
        if existing_user.email == user.email: #type:ignore
            raise HTTPException(status_code=400, detail="Email already registered")
        if existing_user.username == user.username:#type:ignore
            raise HTTPException(status_code=400, detail="Username already taken")

    allowed_roles = ["student", "librarian"]
    role = user.role if user.role in allowed_roles else "student"

    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw, role=role)
    
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@auth_router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.email == user.username) | (User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = jwt.encode({"sub": db_user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

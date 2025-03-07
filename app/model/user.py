from sqlalchemy import Column, Integer, String,UniqueConstraint
from app.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)  # Ensure username is unique
    email = Column(String(100), unique=True, nullable=False)  # Ensure email is unique
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student")  # Can be "student", "librarian", "admin"

    __table_args__ = (UniqueConstraint('username', 'email'),)

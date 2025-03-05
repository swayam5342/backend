from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    genre = Column(String(255), nullable=False)
    copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    rating = Column(Float, default=0.0)
    borrowed_count = Column(Integer, default=0)


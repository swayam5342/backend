from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str
    genre: str
    copies: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    copies: Optional[int] = None

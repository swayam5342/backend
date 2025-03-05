from pydantic import BaseModel

class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str
    genre: str
    copies: int

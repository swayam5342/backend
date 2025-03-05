from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.model.book import Book
from app.service.auth import require_role
from app.schema.book import BookCreate
from typing import List, Optional

book_router = APIRouter()

@book_router.get("/books")
def get_book(db: Session = Depends(get_db)):
    book = db.query(Book).all()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.get("/books/{book_id}")
def get_book_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@book_router.get("/books/search")
def search_books(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None, description="Search by book title"),
    author: Optional[str] = Query(None, description="Search by author"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    available: Optional[bool] = Query(None, description="Filter by availability")
):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if available is not None:
        query = query.filter(Book.available_copies > 0 if available else Book.available_copies == 0)
    results = query.all()
    return results


@book_router.post("/books/", dependencies=[Depends(require_role("librarian"))])
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict(), available_copies=book.copies)
    db.add(db_book)
    db.commit()
    return {"message": "Book added successfully"}

@book_router.delete("/books/{book_id}", dependencies=[Depends(require_role("librarian"))])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

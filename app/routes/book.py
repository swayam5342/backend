from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.model.book import Book
from app.service.auth import require_role
from app.schema.book import BookCreate,BookUpdate
from typing import Optional

book_router = APIRouter()

@book_router.get("/books")
def get_book(db: Session = Depends(get_db)):
    book = db.query(Book).all()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.get("/books/find")
def search_books(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None, description="Search by book title"),
    author: Optional[str] = Query(None, description="Search by author"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    available: Optional[bool] = Query(None, description="Filter by availability")):
    print(f"%{title}%")
    query = db.query(Book)
    print(f"%{title}%")
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if available is not None:
        query = query.filter(Book.available_copies > 0 if available else Book.available_copies == 0)
    return query.all()


@book_router.get("/books/{book_id}")
def get_book_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book



@book_router.post("/books", dependencies=[Depends(require_role("librarian"))])
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_book:
        return {"message": "Book already exists in the database."}
    db_book = Book(**book.model_dump, available_copies=book.copies)
    db.add(db_book)
    db.commit()
    return {"message": "Book added successfully"}

@book_router.put("/books/{book_id}", dependencies=[Depends(require_role("librarian"))])
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db)
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book_update.title:
        db_book.title = book_update.title #type:ignore
    if book_update.author:
        db_book.author = book_update.author #type:ignore
    if book_update.genre:
        db_book.genre = book_update.genre #type:ignore
    if book_update.copies:
        db_book.copies = book_update.copies #type:ignore
        db_book.available_copies = book_update.copies #type:ignore
    db.commit()
    db.refresh(db_book)
    return {"message": "Book updated successfully", "book": db_book}

@book_router.delete("/books/{book_id}", dependencies=[Depends(require_role("librarian"))])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

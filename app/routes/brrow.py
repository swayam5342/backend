from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.service.auth import get_current_user, require_role
from app.model.brrow import BorrowedBooks
from app.model.book import Book
from app.model.user import User
from app.database import get_db
from datetime import datetime, timedelta

borrow_router = APIRouter()

@borrow_router.post("/borrow/{book_id}")
def borrow_book(book_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.available_copies < 1: #type:ignore
        raise HTTPException(status_code=400, detail="Book not available")
    borrowed = BorrowedBooks(
        user_id=current_user.id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    book.available_copies -= 1 #type:ignore
    db.add(borrowed)
    db.commit()
    return {"message": f"Book '{book.title}' borrowed successfully!"}


@borrow_router.post("/return/{book_id}")
def return_book(book_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    borrowed = db.query(BorrowedBooks).filter(
        BorrowedBooks.book_id == book_id,
        BorrowedBooks.user_id == current_user.id,
        BorrowedBooks.is_returned == False
    ).first()
    if not borrowed:
        raise HTTPException(status_code=400, detail="No active borrow record found")
    borrowed.return_date = datetime.utcnow() #type:ignore
    borrowed.is_returned = True #type:ignore
    if borrowed.return_date > borrowed.due_date:#type:ignore
        days_late = (borrowed.return_date - borrowed.due_date).days
        borrowed.fine = days_late * 5
    book = db.query(Book).filter(Book.id == book_id).first()
    book.available_copies += 1#type:ignore
    db.commit()
    return {"message": "Book returned successfully!", "fine": borrowed.fine}


@borrow_router.get("/borrowed", dependencies=[Depends(require_role("student"))])
def get_borrowed_books(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    borrowed_books = db.query(BorrowedBooks).filter(
        BorrowedBooks.user_id == current_user.id
    ).all()
    if not borrowed_books:
        raise HTTPException(status_code=404, detail="No borrowed books found")
    return borrowed_books

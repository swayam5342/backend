from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BorrowBase(BaseModel):
    book_id: int
    borrow_date: datetime
    due_date: datetime
    is_returned: bool
    fine: float = 0.0

class BorrowResponse(BorrowBase):
    title: str

    class Config:
        orm_mode = True

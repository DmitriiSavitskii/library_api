from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BorrowBase(BaseModel):
    book_id: int
    reader_id: int


class BorrowCreate(BorrowBase):
    pass


class BorrowOut(BorrowBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime]

    class Config:
        from_attributes = True

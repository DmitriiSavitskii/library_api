from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

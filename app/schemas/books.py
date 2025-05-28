from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    release_date: Optional[int] = None
    isbn: Optional[str] = None
    copies: int = Field(default=1, ge=0)
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True
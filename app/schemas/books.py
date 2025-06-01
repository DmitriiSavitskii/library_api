from pydantic import BaseModel, Field, ConfigDict
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
    title: Optional[str] = None
    author: Optional[str] = None
    release_date: Optional[int] = None
    isbn: Optional[str] = None
    copies: Optional[int] = None
    description: Optional[str] = None


class BookOut(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class ReaderBase(BaseModel):
    name: str
    email: EmailStr


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class ReaderOut(ReaderBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

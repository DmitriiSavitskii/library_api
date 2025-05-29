from pydantic import BaseModel, EmailStr


class ReaderBase(BaseModel):
    name: str
    email: EmailStr


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(ReaderBase):
    pass


class ReaderOut(ReaderBase):
    id: int

    class Config:
        from_attributes = True

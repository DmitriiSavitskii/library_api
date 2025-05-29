from app.database import Base
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[int | None] = mapped_column(nullable=True)
    isbn: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    copies: Mapped[int] = mapped_column(default=1, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    borrows: Mapped[List["Borrow"]] = relationship(back_populates="book")

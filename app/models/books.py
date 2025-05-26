from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[int | None] = mapped_column(nullable=True)
    isbn: Mapped[str | None] = mapped_column(unique=True, nullable=True)
    copies: Mapped[int] = mapped_column(default=1, nullable=False)
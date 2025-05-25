from database import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id", ondelete="CASCADE"), nullable=False)
    borrow_date: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    return_date: Mapped[datetime | None] = mapped_column(nullable=True)

    book: Mapped["Book"] = relationship(back_populates="borrows")
    reader: Mapped["Reader"] = relationship(back_populates="borrows")
from app.database import Base
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    borrows: Mapped[List["Borrow"]] = relationship(back_populates="reader")

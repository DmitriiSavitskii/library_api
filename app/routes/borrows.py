from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from datetime import datetime, timezone
from app.database import SessionDepends
from app.models.books import Book
from app.models.borrows import Borrow
from app.models.users import User
from app.core.security import get_current_user
from app.schemas.borrows import BorrowBase


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def issue_book(
    data: BorrowBase,
    session: SessionDepends,
    current_user: User = Depends(get_current_user)
):
    book = await session.get(Book, data.book_id)

    if not book or book.copies < 1:
        raise HTTPException(
            status_code=400,
            detail="No available copies for this book.")

    result = await session.execute(
        select(Borrow).where(
            Borrow.reader_id == data.reader_id,
            Borrow.return_date.is_(None)))
    active_borrows = result.scalars().all()

    if len(active_borrows) >= 3:
        raise HTTPException(
            status_code=400,
            detail="Reader has already borrowed the maximum number of books.")

    book.copies -= 1
    borrow = Borrow(
        book_id=data.book_id,
        reader_id=data.reader_id,
        borrow_date=datetime.now(timezone.utc).replace(tzinfo=None),
        return_date=None)
    session.add(borrow)
    await session.commit()
    return {"message": "Book successfully issued to reader"}


@router.post("/return", status_code=status.HTTP_200_OK)
async def return_book(
    data: BorrowBase,
    session: SessionDepends,
    current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Borrow).where(
            Borrow.book_id == data.book_id,
            Borrow.reader_id == data.reader_id,
            Borrow.return_date.is_(None)))
    borrow = result.scalars().first()

    if not borrow:
        raise HTTPException(
            status_code=400,
            detail="No active borrowing found for this book and reader.")

    borrow.return_date = datetime.now(timezone.utc).replace(tzinfo=None)
    book = await session.get(Book, data.book_id)
    book.copies += 1

    await session.commit()
    return {"message": "Book successfully returned"}

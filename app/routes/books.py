from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import SessionDepends
from app.core.security import get_current_user
from app.models.users import User
from app.schemas.books import *
from app.models.books import Book

router = APIRouter()


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, session: SessionDepends, current_user: User = Depends(get_current_user)):
    if book_in.isbn:
        result = await session.execute(select(Book).where(Book.isbn == book_in.isbn))
        existing_book = result.scalars().first()
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    book = Book(**book_in.model_dump())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


@router.get("/", response_model=list[BookOut])
async def list_books(session: SessionDepends, current_user: User = Depends(get_current_user)):
    result = await session.execute(select(Book))
    return result.scalars().all()


@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, session: SessionDepends, current_user: User = Depends(get_current_user)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookOut)
async def update_book(book_id: int, book_in: BookUpdate, session: SessionDepends, current_user: User = Depends(get_current_user)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in book_in.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    await session.commit()
    await session.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session: SessionDepends, current_user: User = Depends(get_current_user)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(book)
    await session.commit()

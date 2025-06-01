from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.models.readers import Reader
from app.schemas.readers import ReaderCreate, ReaderUpdate, ReaderOut
from app.database import SessionDepends
from app.core.security import get_current_user
from app.models.users import User
from app.models.books import Book
from app.models.borrows import Borrow
from app.schemas.books import BookOut


router = APIRouter()


@router.post("/", response_model=ReaderOut,
             status_code=status.HTTP_201_CREATED)
async def create_reader(
    reader_in: ReaderCreate,
    session: SessionDepends,
    current_user: User = Depends(get_current_user)
):
    existing = await session.execute(
        select(Reader).where(
            Reader.email == reader_in.email))
    if existing.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="Reader with this email already exists")

    reader = Reader(**reader_in.model_dump())
    session.add(reader)
    await session.commit()
    await session.refresh(reader)
    return reader


@router.get("/", response_model=list[ReaderOut])
async def get_readers(
    session: SessionDepends,
    current_user: User = Depends(get_current_user)
):
    result = await session.execute(select(Reader))
    return result.scalars().all()


@router.get("/{reader_id}", response_model=ReaderOut)
async def get_reader(
    reader_id: int,
    session: SessionDepends,
    current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Reader).where(Reader.id == reader_id))
    reader = result.scalars().first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@router.get("/{reader_id}/borrowed", response_model=list[BookOut])
async def get_reader_borrowed_books(
    reader_id: int,
    session: SessionDepends,
    current_user: User = Depends(get_current_user)
):

    result = await session.execute(
        select(Book).join(Borrow).where(
            Borrow.reader_id == reader_id,
            Borrow.return_date.is_(None)
        )
    )
    books = result.scalars().all()

    if not books:
        raise HTTPException(
            status_code=404,
            detail="No active borrowings found for this reader")

    return books


@router.put("/{reader_id}", response_model=ReaderOut)
async def update_reader(
    reader_id: int,
    reader_update: ReaderUpdate,
    session: SessionDepends,
    current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Reader).where(Reader.id == reader_id))
    reader = result.scalars().first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    update_data = reader_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reader, key, value)

    await session.commit()
    await session.refresh(reader)
    return reader


@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reader(
    reader_id: int,
    session: SessionDepends,
    current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Reader).where(Reader.id == reader_id))
    reader = result.scalars().first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    await session.delete(reader)
    await session.commit()

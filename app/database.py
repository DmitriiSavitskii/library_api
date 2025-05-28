from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from fastapi import Depends


async_engine = create_async_engine(url=settings.DATABASE_URL, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=True)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with async_session() as session:
        yield session

SessionDepends = Annotated[AsyncSession, Depends(get_session)]
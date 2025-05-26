from app.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


async_engine = create_async_engine(url=settings.DATABASE_URL, echo=False)
async_session = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass
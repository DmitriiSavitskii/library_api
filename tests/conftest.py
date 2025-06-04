import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import uuid

from app.main import app
from app.database import Base, get_session

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres_test:5432/library_postgres_test"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def prepare_database():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session(prepare_database):
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_data():
    return {
        "email": f"user_{uuid.uuid4()}@example.com",
        "password": "password123"
    }


@pytest_asyncio.fixture
async def registered_user(client: AsyncClient, user_data):
    await client.post("/auth/register", json=user_data)
    response = await client.post("/auth/login", json=user_data)
    token = response.json()["access_token"]
    return {
        "headers": {"Authorization": f"Bearer {token}"},
        "user_data": user_data
    }

@pytest_asyncio.fixture
async def test_reader(client: AsyncClient, registered_user):
    headers = registered_user["headers"]
    reader_data = {
        "name": "Test Reader",
        "email": "reader@example.com"
    }
    response = await client.post(
        "/readers/", json=reader_data, headers=headers)
    return response.json()


@pytest_asyncio.fixture
async def test_books(client: AsyncClient, registered_user):
    headers = registered_user["headers"]
    books = []
    for i in range(6):
        data = {
            "title": f"Book {i}",
            "author": f"Author {i}",
            "isbn": f"1234567890{i}",
            "copies": 1
        }
        response = await client.post("/books/", json=data, headers=headers)
        books.append(response.json())
    return books


@pytest_asyncio.fixture
async def book_with_no_copies(client: AsyncClient,
                              registered_user, test_reader):
    headers = registered_user["headers"]
    book_data = {
        "title": "No Copies Book",
        "author": "Author X",
        "isbn": "0000000000",
        "copies": 1
    }
    response = await client.post("/books/", json=book_data, headers=headers)
    book = response.json()

    await client.post("/borrows/", json={
        "book_id": book["id"],
        "reader_id": test_reader["id"]
    }, headers=headers)

    return book


@pytest_asyncio.fixture
async def borrowed_book(session, test_books, test_reader):
    from app.models.borrows import Borrow
    from datetime import datetime, timezone

    borrow = Borrow(
        book_id=test_books[0]["id"],
        reader_id=test_reader["id"],
        borrow_date=datetime.now(timezone.utc).replace(tzinfo=None),
        return_date=None
    )
    session.add(borrow)
    await session.commit()
    return borrow

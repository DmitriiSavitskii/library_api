import pytest
from httpx import AsyncClient


class TestBorrowAPI:

    @pytest.mark.asyncio
    async def test_borrow_book_success(self, client: AsyncClient, registered_user, test_reader, test_books):
        headers = registered_user["headers"]
        book = test_books[0]

        response = await client.post("/borrows/", json={
            "book_id": book["id"],
            "reader_id": test_reader["id"]
        }, headers=headers)

        assert response.status_code == 201
        assert response.json()["message"] == "Book successfully issued to reader"

        response = await client.get(f"/books/{book['id']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["copies"] == book["copies"] - 1

    @pytest.mark.asyncio
    async def test_borrow_book_no_copies(self, client: AsyncClient, registered_user, test_reader, book_with_no_copies):
        headers = registered_user["headers"]

        response = await client.post("/borrows/", json={
            "book_id": book_with_no_copies["id"],
            "reader_id": test_reader["id"]
        }, headers=headers)

        assert response.status_code == 400
        assert response.json()["detail"] == "No available copies for this book."

    @pytest.mark.asyncio
    async def test_borrow_more_than_three_books(self, client: AsyncClient, registered_user, test_reader, test_books):
        headers = registered_user["headers"]

        for i in range(3):
            response = await client.post("/borrows/", json={
                "book_id": test_books[i]["id"],
                "reader_id": test_reader["id"]
            }, headers=headers)
            assert response.status_code == 201

        response = await client.post("/borrows/", json={
            "book_id": test_books[3]["id"],
            "reader_id": test_reader["id"]
        }, headers=headers)

        assert response.status_code == 400
        assert response.json()["detail"] == "Reader has already borrowed the maximum number of books."

    @pytest.mark.asyncio
    async def test_return_book_success(self, client: AsyncClient, registered_user, test_reader, test_books):
        headers = registered_user["headers"]
        book = test_books[4]

        await client.post("/borrows/", json={
            "book_id": book["id"],
            "reader_id": test_reader["id"]
        }, headers=headers)

        response = await client.post("/borrows/return", json={
            "book_id": book["id"],
            "reader_id": test_reader["id"]
        }, headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "Book successfully returned"

    @pytest.mark.asyncio
    async def test_return_book_invalid(self, client: AsyncClient, registered_user, test_reader, test_books):
        headers = registered_user["headers"]
        book = test_books[5]

        response = await client.post("/borrows/return", json={
            "book_id": book["id"],
            "reader_id": test_reader["id"]
        }, headers=headers)

        assert response.status_code == 400
        assert response.json()["detail"] == "No active borrowing found for this book and reader."

    @pytest.mark.asyncio
    async def test_protected_borrow_endpoint_no_token(self, client: AsyncClient, test_reader, test_books):
        response = await client.post("/borrows/", json={
            "book_id": test_books[0]["id"],
            "reader_id": test_reader["id"]
        })

        assert response.status_code == 401

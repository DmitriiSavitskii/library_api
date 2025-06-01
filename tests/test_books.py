# import pytest
# from httpx import AsyncClient


# class TestBooksAPI:

#     @pytest.mark.asyncio
#     async def test_create_book(self, client: AsyncClient, registered_user):
#         headers = registered_user["headers"]
#         book_data = {
#             "title": "Test Book",
#             "author": "Author Name",
#             "isbn": "1234567890123"
#         }

#         response = await client.post("/books/", json=book_data, headers=headers)
#         assert response.status_code == 201

#         data = response.json()
#         assert data["title"] == book_data["title"]
#         assert data["author"] == book_data["author"]
#         assert data["isbn"] == book_data["isbn"]

#     @pytest.mark.asyncio
#     async def test_get_all_books(self, client: AsyncClient):
#         response = await client.get("/books/")
#         assert response.status_code == 200
#         assert isinstance(response.json(), list)

#     @pytest.mark.asyncio
#     async def test_get_book_by_id(self, client: AsyncClient, registered_user):
#         headers = registered_user["headers"]
#         book_data = {
#             "title": "Book ID Test",
#             "author": "Author B",
#             "isbn": "9876543210987"
#         }

#         response = await client.post("/books/", json=book_data, headers=headers)
#         assert response.status_code == 201

#         book_id = response.json()["id"]
#         response = await client.get(f"/books/{book_id}", headers=headers)
#         assert response.status_code == 200
#         assert response.json()["id"] == book_id

#     @pytest.mark.asyncio
#     async def test_update_book(self, client: AsyncClient, registered_user):
#         headers = registered_user["headers"]
#         book_data = {
#             "title": "Old Title",
#             "author": "Author Old",
#             "isbn": "1111222233334"
#         }
#         response = await client.post("/books/", json=book_data, headers=headers)
#         assert response.status_code == 201

#         book_id = response.json()["id"]
#         update_data = {"title": "New Title"}
#         response = await client.put(f"/books/{book_id}", json=update_data, headers=headers)
#         assert response.status_code == 200
#         assert response.json()["title"] == "New Title"

#     @pytest.mark.asyncio
#     async def test_delete_book(self, client: AsyncClient, registered_user):
#         headers = registered_user["headers"]
#         book_data = {
#             "title": "Delete Me",
#             "author": "Author D",
#             "isbn": "9999999999999"
#         }
#         response = await client.post("/books/", json=book_data, headers=headers)
#         book_id = response.json()["id"]
#         assert response.status_code == 201

#         response = await client.delete(f"/books/{book_id}", headers=headers)
#         assert response.status_code == 204

#         get_resp = await client.get(f"/books/{book_id}", headers=headers)
#         assert get_resp.status_code == 404

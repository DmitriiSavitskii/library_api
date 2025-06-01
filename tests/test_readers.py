import pytest
from httpx import AsyncClient


class TestReadersAPI:

    @pytest.mark.asyncio
    async def test_create_reader(self, client: AsyncClient, registered_user):
        headers = registered_user["headers"]
        data = {
            "name": "John Reader",
            "email": "john.reader@example.com"
        }
        response = await client.post("/readers/", json=data, headers=headers)
        assert response.status_code == 201
        assert response.json()["email"] == data["email"]

    @pytest.mark.asyncio
    async def test_get_readers(self, client: AsyncClient, registered_user, test_reader):
        headers = registered_user["headers"]
        response = await client.get("/readers/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert any(r["email"] == test_reader["email"] for r in response.json())

    @pytest.mark.asyncio
    async def test_get_reader_by_id(self, client: AsyncClient, registered_user, test_reader):
        headers = registered_user["headers"]
        reader_id = test_reader["id"]
        response = await client.get(f"/readers/{reader_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["id"] == reader_id

    @pytest.mark.asyncio
    async def test_update_reader(self, client: AsyncClient, registered_user, test_reader):
        headers = registered_user["headers"]
        reader_id = test_reader["id"]
        update_data = {"name": "Updated Reader"}
        response = await client.put(f"/readers/{reader_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Reader"
        assert response.json()["email"] == "reader@example.com"

    @pytest.mark.asyncio
    async def test_delete_reader(self, client: AsyncClient, registered_user, test_reader):
        headers = registered_user["headers"]
        reader_id = test_reader["id"]
        response = await client.delete(f"/readers/{reader_id}", headers=headers)
        assert response.status_code == 204

        response = await client.get(f"/readers/{reader_id}", headers=headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_reader_borrowed_books(self, client, registered_user, test_reader, borrowed_book):
        headers = registered_user["headers"]
        response = await client.get(f"/readers/{test_reader['id']}/borrowed", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == borrowed_book.book_id

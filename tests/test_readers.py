import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestReadersAPI:

    async def test_create_reader(self, client: AsyncClient, registered_user):
        headers = registered_user["headers"]
        reader_data = {
            "name": "Alice Reader",
            "email": "alice.reader@example.com"
        }

        response = await client.post("/readers/", json=reader_data, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alice Reader"
        assert data["email"] == "alice.reader@example.com"
        assert "id" in data

    async def test_create_reader_duplicate_email(self, client: AsyncClient, registered_user):
        headers = registered_user["headers"]
        email = "duplicate@example.com"
        reader_data = {"name": "First Reader", "email": email}

        resp1 = await client.post("/readers/", json=reader_data, headers=headers)
        assert resp1.status_code == 201

        resp2 = await client.post("/readers/", json=reader_data, headers=headers)
        assert resp2.status_code == 400

    async def test_get_all_readers(self, client: AsyncClient, registered_user, test_reader):
        headers = registered_user["headers"]

        response = await client.get("/readers/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(r["id"] == test_reader["id"] for r in data)

    async def test_get_reader_by_id(self, client: AsyncClient, registered_user, test_reader):
        headers = registered_user["headers"]
        reader_id = test_reader["id"]

        response = await client.get(f"/readers/{reader_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == reader_id
        assert data["email"] == test_reader["email"]

    async def test_update_reader(self, client: AsyncClient, registered_user, test_reader):
        headers = registered_user["headers"]
        updated_data = {
            "name": "Updated Name",
        }

        response = await client.put(f"/readers/{test_reader['id']}", json=updated_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    async def test_delete_reader(self, client: AsyncClient, registered_user, test_reader):
        headers = registered_user["headers"]
        reader_id = test_reader["id"]

        response = await client.delete(f"/readers/{reader_id}", headers=headers)
        assert response.status_code == 204

        get_resp = await client.get(f"/readers/{reader_id}", headers=headers)
        assert get_resp.status_code == 404

    async def test_unauthorized_access_to_readers(self, client: AsyncClient, test_reader):
        response = await client.get(f"/readers/{test_reader['id']}")
        assert response.status_code == 401

        response = await client.post("/readers/", json={"name": "NoAuth", "email": "noauth@example.com"})
        assert response.status_code == 401

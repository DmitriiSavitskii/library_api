# import pytest
# from httpx import AsyncClient
# from jose import jwt
# from app.config import settings


# class TestRegister:

#     @pytest.mark.asyncio
#     async def test_register(self, client: AsyncClient, user_data):
#         response = await client.post("/auth/register", json=user_data)
#         assert response.status_code == 200

#         token_data = response.json()
#         assert "access_token" in token_data

#         payload = jwt.decode(
#             token_data["access_token"],
#             settings.SECRET_KEY,
#             algorithms=[settings.ALGORITHM],
#         )
#         assert payload["sub"] == user_data["email"]

#     @pytest.mark.asyncio
#     async def test_register_existing_email(self, client: AsyncClient, user_data):
#         response = await client.post("/auth/register", json=user_data)
#         assert response.status_code == 200

#         response = await client.post("/auth/register", json=user_data)
#         assert response.status_code == 400
#         assert response.json()["detail"] == "Email already registered"


# class TestLogin:

#     @pytest.mark.asyncio
#     async def test_login(self, client: AsyncClient, user_data):
#         response = await client.post("/auth/register", json=user_data)
#         assert response.status_code == 200

#         token_data = response.json()
#         assert "access_token" in token_data

#         payload = jwt.decode(
#             token_data["access_token"],
#             settings.SECRET_KEY,
#             algorithms=[settings.ALGORITHM],
#         )
#         assert payload["sub"] == user_data["email"]

#     @pytest.mark.asyncio
#     async def test_login_wrong_password(self, client: AsyncClient, user_data):
#         response = await client.post("/auth/register", json=user_data)
#         assert response.status_code == 200

#         response = await client.post("/auth/login", json={
#             "email": "user@example.com",
#             "password": "wrongpassword"
#         })
#         assert response.status_code == 401
#         assert response.json()["detail"] == "Invalid credentials"

#     @pytest.mark.asyncio
#     async def test_login_nonexistent_user(self, client: AsyncClient):
#         response = await client.post("/auth/login", json={
#             "email": "nouser@example.com",
#             "password": "any"
#         })
#         assert response.status_code == 401
#         assert response.json()["detail"] == "Invalid credentials"


# class TestProtectedEndpoint:

#     @pytest.mark.asyncio
#     async def test_access_with_valid_token(self, client: AsyncClient, registered_user):
#         headers = registered_user["headers"]
#         response = await client.get("/auth/me", headers=headers)
#         assert response.status_code == 200
#         assert response.json()["email"] == registered_user["user_data"]["email"]

#     @pytest.mark.asyncio
#     async def test_access_with_invalid_token(self, client: AsyncClient):
#         headers = {"Authorization": "Bearer invalidtoken"}
#         response = await client.get("/auth/me", headers=headers)
#         assert response.status_code == 401

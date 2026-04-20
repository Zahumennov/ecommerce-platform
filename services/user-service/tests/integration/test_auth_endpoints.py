import pytest
from httpx import AsyncClient


class TestRegisterEndpoint:
    async def test_register_success(self, client: AsyncClient):
        response = await client.post("/auth/register", json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert "id" in data
        assert "hashed_password" not in data
        assert data["is_active"] is True
        assert data["is_verified"] is False

    async def test_register_duplicate_email(self, client: AsyncClient):
        payload = {
            "email": "duplicate@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        }
        await client.post("/auth/register", json=payload)
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 409

    async def test_register_invalid_email(self, client: AsyncClient):
        response = await client.post("/auth/register", json={
            "email": "not-an-email",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        })
        assert response.status_code == 422

    async def test_register_weak_password_no_uppercase(self, client: AsyncClient):
        response = await client.post("/auth/register", json={
            "email": "test2@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "weakpass1",
        })
        assert response.status_code == 422

    async def test_register_weak_password_no_digit(self, client: AsyncClient):
        response = await client.post("/auth/register", json={
            "email": "test3@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "WeakPassNoDigit",
        })
        assert response.status_code == 422

    async def test_register_short_password(self, client: AsyncClient):
        response = await client.post("/auth/register", json={
            "email": "test4@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Sh0rt",
        })
        assert response.status_code == 422


class TestLoginEndpoint:
    async def test_login_success(self, client: AsyncClient):
        await client.post("/auth/register", json={
            "email": "login@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        })
        response = await client.post("/auth/login", data={
            "username": "login@example.com",
            "password": "SecurePass1",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient):
        await client.post("/auth/register", json={
            "email": "login2@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        })
        response = await client.post("/auth/login", data={
            "username": "login2@example.com",
            "password": "WrongPass1",
        })
        assert response.status_code == 401

    async def test_login_nonexistent_user(self, client: AsyncClient):
        response = await client.post("/auth/login", data={
            "username": "nobody@example.com",
            "password": "SecurePass1",
        })
        assert response.status_code == 401


class TestGetMeEndpoint:
    async def test_get_me_success(self, client: AsyncClient):
        await client.post("/auth/register", json={
            "email": "me@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        })
        login = await client.post("/auth/login", data={
            "username": "me@example.com",
            "password": "SecurePass1",
        })
        token = login.json()["access_token"]
        response = await client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "me@example.com"

    async def test_get_me_no_token(self, client: AsyncClient):
        response = await client.get("/users/me")
        assert response.status_code == 401

    async def test_get_me_invalid_token(self, client: AsyncClient):
        response = await client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalidtoken"},
        )
        assert response.status_code == 401

class TestUpdateMeEndpoint:
    async def test_update_me_success(self, client: AsyncClient):
        await client.post("/auth/register", json={
            "email": "update@example.com",
            "first_name": "Old",
            "last_name": "Name",
            "password": "SecurePass1",
        })
        login = await client.post("/auth/login", data={
            "username": "update@example.com",
            "password": "SecurePass1",
        })
        token = login.json()["access_token"]
        response = await client.patch(
            "/users/me",
            json={"first_name": "New"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["first_name"] == "New"
        assert response.json()["last_name"] == "Name"

    async def test_update_me_no_token(self, client: AsyncClient):
        response = await client.patch("/users/me", json={"first_name": "New"})
        assert response.status_code == 401


class TestDeleteMeEndpoint:
    async def test_delete_me_success(self, client: AsyncClient):
        await client.post("/auth/register", json={
            "email": "delete@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        })
        login = await client.post("/auth/login", data={
            "username": "delete@example.com",
            "password": "SecurePass1",
        })
        token = login.json()["access_token"]
        response = await client.delete(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Account deleted successfully"

    async def test_delete_me_no_token(self, client: AsyncClient):
        response = await client.delete("/users/me")
        assert response.status_code == 401


class TestGetUserEndpoint:
    async def test_get_user_by_id_success(self, client: AsyncClient):
        register = await client.post("/auth/register", json={
            "email": "getuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        })
        user_id = register.json()["id"]
        login = await client.post("/auth/login", data={
            "username": "getuser@example.com",
            "password": "SecurePass1",
        })
        token = login.json()["access_token"]
        response = await client.get(
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    async def test_get_user_not_found(self, client: AsyncClient):
        await client.post("/auth/register", json={
            "email": "getuser2@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "SecurePass1",
        })
        login = await client.post("/auth/login", data={
            "username": "getuser2@example.com",
            "password": "SecurePass1",
        })
        token = login.json()["access_token"]
        response = await client.get(
            "/users/00000000-0000-0000-0000-000000000000",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
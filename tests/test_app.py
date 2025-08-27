import pytest
from httpx import AsyncClient
from app.main import app
from app.database import engine
import asyncio


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root(client):
    r = await client.get("/")
    assert r.status_code == 200
    assert "Hello" in r.json()["msg"]


@pytest.mark.asyncio
async def test_register_login_and_task_flow(client):
    email = "test_async@example.com"
    password = "strongpassword"

    r = await client.post("/register", json={"email": email, "password": password})
    assert r.status_code == 200

    r = await client.post("/login", data={"username": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    r = await client.post("/tasks", json={"title": "Async Task"}, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Async Task"

    r = await client.get("/tasks", headers=headers)
    assert r.status_code == 200
    tasks = r.json()
    assert len(tasks) >= 1
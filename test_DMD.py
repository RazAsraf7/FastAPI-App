import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from DMD import app  # Assuming 'app' is your FastAPI instance
from urllib.parse import quote

client = TestClient(app)

def test_read_main():
    response = client.get("/root")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        try:
            response = await ac.post("/register", data={
                "First_Name": "Test",
                "Last_Name": "User",
                "User_Name": "testuser",
                "Password": "TestPassword1",
                "Email": "testuser@example.com",
                "Address": "123 Test St",
                "City": "Tel Aviv-Yafo",
                "Gender": "Other",
                "Phone_Number": "1234567890"
            })
            assert response.status_code == 302, f"Response: {response.content.decode()}"

            # Adjust the expected location to match actual URL encoding
            actual_location = response.headers["location"]
            expected_location = (
                f"/register_success?User_Name=testuser&Full_Name={quote('Test User')}&"
                f"Email=testuser@example.com&City={quote('Tel Aviv-Yafo')}&"
                f"Gender={quote('Other')}"
            )

            print(f"Actual location: {actual_location}")
            print(f"Expected location: {expected_location}")

            assert actual_location == expected_location

        except AssertionError as e:
            if "Username already exists" in str(response.content.decode()):
                pass  # Move forward if the username already exists
            else:
                raise e  # Re-raise the exception if it's a different error

@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/login", data={
            "User_Name": "testuser",
            "Password": "TestPassword1"
        })
    assert response.status_code == 303, f"Response: {response.content.decode()}"

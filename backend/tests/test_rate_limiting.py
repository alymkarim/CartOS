import pytest
from app.models import User
from app.security import hash_password


class TestRateLimiting:
    def test_login_rate_limit(self, client, db):
        user = User(
            email="ratelimit@example.com",
            hashed_password=hash_password("StrongPass123"),
            role="customer",
        )
        db.add(user)
        db.commit()

        for i in range(10):
            response = client.post(
                "/api/auth/login",
                data={
                    "username": "ratelimit@example.com",
                    "password": "StrongPass123",
                },
            )
            assert response.status_code == 200

        response = client.post(
            "/api/auth/login",
            data={
                "username": "ratelimit@example.com",
                "password": "StrongPass123",
            },
        )
        assert response.status_code == 429
        assert response.json()["detail"] == "Too many requests. Please try again later."

    def test_register_rate_limit(self, client, db):
        for i in range(5):
            response = client.post(
                "/api/auth/register",
                json={
                    "email": f"test{i}@example.com",
                    "password": "StrongPass123",
                },
            )
            assert response.status_code == 201

        response = client.post(
            "/api/auth/register",
            json={
                "email": "test6@example.com",
                "password": "StrongPass123",
            },
        )
        assert response.status_code == 429
        assert response.json()["detail"] == "Too many requests. Please try again later."

    def test_forgot_password_rate_limit(self, client, db):
        user = User(
            email="forgot@example.com",
            hashed_password=hash_password("StrongPass123"),
            role="customer",
        )
        db.add(user)
        db.commit()

        for i in range(5):
            response = client.post(
                "/api/auth/forgot-password",
                json={"email": "forgot@example.com"},
            )
            assert response.status_code == 200

        response = client.post(
            "/api/auth/forgot-password",
            json={"email": "forgot@example.com"},
        )
        assert response.status_code == 429
        assert response.json()["detail"] == "Too many requests. Please try again later."

import pytest
from app.security import validate_password_strength, hash_password, verify_password
from app.models import User, PasswordReset


class TestPasswordValidation:
    def test_valid_password(self):
        assert validate_password_strength("ValidPass123") is None

    def test_too_short(self):
        error = validate_password_strength("Short1")
        assert error is not None
        assert "at least 8 characters" in error

    def test_no_uppercase(self):
        error = validate_password_strength("lowercase123")
        assert error is not None
        assert "uppercase" in error

    def test_no_lowercase(self):
        error = validate_password_strength("UPPERCASE123")
        assert error is not None
        assert "lowercase" in error

    def test_no_number(self):
        error = validate_password_strength("NoNumberHere")
        assert error is not None
        assert "number" in error

    def test_exactly_8_chars(self):
        assert validate_password_strength("Abcdefg1") is None


class TestRegisterWithValidation:
    def test_register_weak_password_too_short(self, client):
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "weak"},
        )
        assert response.status_code == 422

    def test_register_weak_password_no_uppercase(self, client):
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "lowercase123"},
        )
        assert response.status_code == 400
        assert "uppercase" in response.json()["detail"].lower()

    def test_register_weak_password_no_number(self, client):
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "NoNumberHere"},
        )
        assert response.status_code == 400
        assert "number" in response.json()["detail"].lower()

    def test_register_strong_password(self, client):
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "StrongPass123"},
        )
        assert response.status_code == 201
        assert response.json()["email"] == "test@example.com"


class TestForgotPassword:
    def test_forgot_password_existing_user(self, client, db):
        user = User(
            email="test@example.com",
            hashed_password=hash_password("OldPass123"),
            role="customer",
        )
        db.add(user)
        db.commit()

        response = client.post(
            "/api/auth/forgot-password",
            json={"email": "test@example.com"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["token"] != ""
        assert "reset link" in data["message"]

    def test_forgot_password_nonexistent_user(self, client, db):
        response = client.post(
            "/api/auth/forgot-password",
            json={"email": "nonexistent@example.com"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["token"] == ""
        assert "reset link" in data["message"]


class TestResetPassword:
    def test_reset_password_valid_token(self, client, db):
        user = User(
            email="test@example.com",
            hashed_password=hash_password("OldPass123"),
            role="customer",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        from datetime import datetime, timedelta, timezone
        import secrets

        token = secrets.token_urlsafe(32)
        reset = PasswordReset(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        db.add(reset)
        db.commit()

        response = client.post(
            "/api/auth/reset-password",
            json={"token": token, "password": "NewStrongPass123"},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Password reset successful."

        db.refresh(user)
        assert verify_password("NewStrongPass123", user.hashed_password)

    def test_reset_password_expired_token(self, client, db):
        user = User(
            email="test@example.com",
            hashed_password=hash_password("OldPass123"),
            role="customer",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        from datetime import datetime, timedelta, timezone
        import secrets

        token = secrets.token_urlsafe(32)
        reset = PasswordReset(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )
        db.add(reset)
        db.commit()

        response = client.post(
            "/api/auth/reset-password",
            json={"token": token, "password": "NewStrongPass123"},
        )
        assert response.status_code == 400
        assert "Invalid or expired" in response.json()["detail"]

    def test_reset_password_used_token(self, client, db):
        user = User(
            email="test@example.com",
            hashed_password=hash_password("OldPass123"),
            role="customer",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        from datetime import datetime, timedelta, timezone
        import secrets

        token = secrets.token_urlsafe(32)
        reset = PasswordReset(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            used=True,
        )
        db.add(reset)
        db.commit()

        response = client.post(
            "/api/auth/reset-password",
            json={"token": token, "password": "NewStrongPass123"},
        )
        assert response.status_code == 400
        assert "Invalid or expired" in response.json()["detail"]

    def test_reset_password_weak_password(self, client, db):
        user = User(
            email="test@example.com",
            hashed_password=hash_password("OldPass123"),
            role="customer",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        from datetime import datetime, timedelta, timezone
        import secrets

        token = secrets.token_urlsafe(32)
        reset = PasswordReset(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        db.add(reset)
        db.commit()

        response = client.post(
            "/api/auth/reset-password",
            json={"token": token, "password": "weak"},
        )
        assert response.status_code == 422

import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models import Coupon


def get_auth_header(client, email="couponuser@example.com", password="StrongPass123"):
    client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )
    response = client.post(
        "/api/auth/login",
        data={"username": email, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_coupon(
    db: Session,
    code="SAVE10",
    discount_type="percentage",
    discount_value=10,
    min_order_amount=None,
    max_uses=None,
    uses_count=0,
    expires_at=None,
    is_active=True,
):
    coupon = Coupon(
        code=code,
        discount_type=discount_type,
        discount_value=discount_value,
        min_order_amount=min_order_amount,
        max_uses=max_uses,
        uses_count=uses_count,
        expires_at=expires_at,
        is_active=is_active,
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


class TestCouponModel:
    def test_coupon_creation(self, db):
        coupon = create_coupon(db)
        assert coupon.id is not None
        assert coupon.code == "SAVE10"
        assert coupon.discount_type == "percentage"
        assert coupon.discount_value == 10
        assert coupon.min_order_amount is None
        assert coupon.max_uses is None
        assert coupon.uses_count == 0
        assert coupon.expires_at is None
        assert coupon.is_active is True
        assert coupon.created_at is not None

    def test_coupon_code_unique(self, db):
        create_coupon(db, code="UNIQUE10")
        with pytest.raises(Exception):
            create_coupon(db, code="UNIQUE10")


class TestValidateCoupon:
    def test_validate_valid_percentage_coupon(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="PERCENT20", discount_type="percentage", discount_value=20)
        response = client.post(
            "/api/coupons/validate",
            json={"code": "PERCENT20", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["discount_amount"] == 2000
        assert "save" in data["message"].lower()

    def test_validate_valid_fixed_coupon(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="FIXED500", discount_type="fixed", discount_value=500)
        response = client.post(
            "/api/coupons/validate",
            json={"code": "FIXED500", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["discount_amount"] == 500

    def test_validate_fixed_coupon_capped_at_order_amount(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="BIGFIXED", discount_type="fixed", discount_value=50000)
        response = client.post(
            "/api/coupons/validate",
            json={"code": "BIGFIXED", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["discount_amount"] == 10000

    def test_validate_coupon_case_insensitive(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="UPPER10")
        response = client.post(
            "/api/coupons/validate",
            json={"code": "upper10", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["valid"] is True

    def test_validate_invalid_coupon(self, client):
        headers = get_auth_header(client)
        response = client.post(
            "/api/coupons/validate",
            json={"code": "NONEXISTENT", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert data["discount_amount"] == 0
        assert "invalid" in data["message"].lower()

    def test_validate_inactive_coupon(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="INACTIVE", is_active=False)
        response = client.post(
            "/api/coupons/validate",
            json={"code": "INACTIVE", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "no longer active" in data["message"].lower()

    def test_validate_expired_coupon(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="EXPIRED", expires_at=datetime.now(timezone.utc) - timedelta(days=1))
        response = client.post(
            "/api/coupons/validate",
            json={"code": "EXPIRED", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "expired" in data["message"].lower()

    def test_validate_coupon_max_uses_reached(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="MAXED", max_uses=5, uses_count=5)
        response = client.post(
            "/api/coupons/validate",
            json={"code": "MAXED", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "usage limit" in data["message"].lower()

    def test_validate_coupon_below_min_order_amount(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="MIN100", min_order_amount=10000)
        response = client.post(
            "/api/coupons/validate",
            json={"code": "MIN100", "order_amount": 5000},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert "minimum" in data["message"].lower()

    def test_validate_coupon_requires_auth(self, client, db):
        create_coupon(db, code="NOAUTH")
        response = client.post(
            "/api/coupons/validate",
            json={"code": "NOAUTH", "order_amount": 10000},
        )
        assert response.status_code == 401

    def test_validate_coupon_with_valid_uses_remaining(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="USESLEFT", max_uses=5, uses_count=3)
        response = client.post(
            "/api/coupons/validate",
            json={"code": "USESLEFT", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["valid"] is True

    def test_validate_coupon_not_yet_expired(self, client, db):
        headers = get_auth_header(client)
        create_coupon(db, code="FUTURE", expires_at=datetime.now(timezone.utc) + timedelta(days=30))
        response = client.post(
            "/api/coupons/validate",
            json={"code": "FUTURE", "order_amount": 10000},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["valid"] is True

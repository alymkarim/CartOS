from datetime import datetime, timezone

from app.models import Order


def get_auth_header(client, email="orderuser@example.com", password="StrongPass123"):
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


def create_order(db, user_id, status="pending"):
    order = Order(
        stripe_session_id=f"cs_test_{datetime.now().timestamp()}",
        product_id="desk-lamp",
        quantity=1,
        payment_status="paid",
        amount_total=4999,
        customer_email="test@example.com",
        user_id=user_id,
        status=status,
        status_updated_at=datetime.now(timezone.utc),
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


class TestGetOrders:
    def test_get_orders_returns_status_field(self, client, db):
        headers = get_auth_header(client)
        user = db.query(Order).first()
        response = client.get("/api/orders", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_orders_includes_status(self, client, db):
        headers = get_auth_header(client)
        response = client.get(
            "/api/auth/me",
            headers=headers,
        )
        user_id = response.json()["id"]
        create_order(db, user_id)
        response = client.get("/api/orders", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "pending"
        assert "status_updated_at" in data[0]


class TestUpdateOrderStatus:
    def test_update_order_status(self, client, db):
        headers = get_auth_header(client)
        me_resp = client.get("/api/auth/me", headers=headers)
        user_id = me_resp.json()["id"]
        order = create_order(db, user_id)

        response = client.patch(
            f"/api/orders/{order.id}/status",
            json={"status": "processing"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "processing"
        assert "status_updated_at" in data

    def test_update_order_status_all_valid_statuses(self, client, db):
        headers = get_auth_header(client)
        me_resp = client.get("/api/auth/me", headers=headers)
        user_id = me_resp.json()["id"]

        for new_status in ["processing", "shipped", "delivered"]:
            order = create_order(db, user_id)
            response = client.patch(
                f"/api/orders/{order.id}/status",
                json={"status": new_status},
                headers=headers,
            )
            assert response.status_code == 200
            assert response.json()["status"] == new_status

    def test_update_order_status_invalid_returns_400(self, client, db):
        headers = get_auth_header(client)
        me_resp = client.get("/api/auth/me", headers=headers)
        user_id = me_resp.json()["id"]
        order = create_order(db, user_id)

        response = client.patch(
            f"/api/orders/{order.id}/status",
            json={"status": "invalid_status"},
            headers=headers,
        )
        assert response.status_code == 400
        assert "invalid status" in response.json()["detail"].lower()

    def test_update_order_status_not_found_returns_404(self, client):
        headers = get_auth_header(client)
        response = client.patch(
            "/api/orders/99999/status",
            json={"status": "processing"},
            headers=headers,
        )
        assert response.status_code == 404

    def test_update_order_status_requires_auth(self, client):
        response = client.patch(
            "/api/orders/1/status",
            json={"status": "processing"},
        )
        assert response.status_code == 401

    def test_update_other_users_order_returns_404(self, client, db):
        headers1 = get_auth_header(client, "user1@example.com", "StrongPass123")
        me_resp = client.get("/api/auth/me", headers=headers1)
        user_id = me_resp.json()["id"]
        order = create_order(db, user_id)

        headers2 = get_auth_header(client, "user2@example.com", "StrongPass123")
        response = client.patch(
            f"/api/orders/{order.id}/status",
            json={"status": "shipped"},
            headers=headers2,
        )
        assert response.status_code == 404

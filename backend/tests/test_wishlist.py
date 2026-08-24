import pytest
from app.models import User
from app.security import hash_password


def get_auth_header(client, email="wishlist@example.com", password="StrongPass123"):
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


class TestGetWishlist:
    def test_get_empty_wishlist(self, client):
        headers = get_auth_header(client)
        response = client.get("/api/wishlist", headers=headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_wishlist_requires_auth(self, client):
        response = client.get("/api/wishlist")
        assert response.status_code == 401

    def test_get_wishlist_returns_items(self, client):
        headers = get_auth_header(client)
        client.post("/api/wishlist/desk-lamp", headers=headers)
        client.post("/api/wishlist/mechanical-keyboard", headers=headers)
        response = client.get("/api/wishlist", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        product_ids = {item["product_id"] for item in data}
        assert product_ids == {"desk-lamp", "mechanical-keyboard"}

    def test_get_wishlist_ordered_by_newest(self, client):
        headers = get_auth_header(client)
        client.post("/api/wishlist/desk-lamp", headers=headers)
        client.post("/api/wishlist/mechanical-keyboard", headers=headers)
        response = client.get("/api/wishlist", headers=headers)
        data = response.json()
        assert data[0]["product_id"] == "mechanical-keyboard"
        assert data[1]["product_id"] == "desk-lamp"


class TestAddToWishlist:
    def test_add_to_wishlist(self, client):
        headers = get_auth_header(client)
        response = client.post("/api/wishlist/desk-lamp", headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["product_id"] == "desk-lamp"
        assert "id" in data
        assert "created_at" in data

    def test_add_to_wishlist_requires_auth(self, client):
        response = client.post("/api/wishlist/desk-lamp")
        assert response.status_code == 401

    def test_add_nonexistent_product_returns_404(self, client):
        headers = get_auth_header(client)
        response = client.post("/api/wishlist/nonexistent", headers=headers)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_add_duplicate_returns_409(self, client):
        headers = get_auth_header(client)
        client.post("/api/wishlist/desk-lamp", headers=headers)
        response = client.post("/api/wishlist/desk-lamp", headers=headers)
        assert response.status_code == 409
        assert "already in wishlist" in response.json()["detail"].lower()


class TestRemoveFromWishlist:
    def test_remove_from_wishlist(self, client):
        headers = get_auth_header(client)
        client.post("/api/wishlist/desk-lamp", headers=headers)
        response = client.delete("/api/wishlist/desk-lamp", headers=headers)
        assert response.status_code == 204

    def test_remove_requires_auth(self, client):
        response = client.delete("/api/wishlist/desk-lamp")
        assert response.status_code == 401

    def test_remove_nonexistent_returns_404(self, client):
        headers = get_auth_header(client)
        response = client.delete("/api/wishlist/desk-lamp", headers=headers)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_remove_only_affects_own_wishlist(self, client):
        headers1 = get_auth_header(client, "user1@example.com", "StrongPass123")
        client.post("/api/wishlist/desk-lamp", headers=headers1)
        headers2 = get_auth_header(client, "user2@example.com", "StrongPass123")
        response = client.delete("/api/wishlist/desk-lamp", headers=headers2)
        assert response.status_code == 404

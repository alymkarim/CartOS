import pytest
from app.models import User
from app.security import hash_password


def get_auth_header(client, email="reviewer@example.com", password="StrongPass123"):
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


class TestCreateReview:
    def test_create_review(self, client):
        headers = get_auth_header(client)
        response = client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 5,
                "title": "Great lamp!",
                "comment": "Perfect for my desk.",
            },
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["product_id"] == "desk-lamp"
        assert data["rating"] == 5
        assert data["title"] == "Great lamp!"
        assert data["comment"] == "Perfect for my desk."
        assert data["user_email"] == "reviewer@example.com"
        assert "id" in data
        assert "created_at" in data

    def test_create_review_requires_auth(self, client):
        response = client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 5,
                "title": "Great lamp!",
                "comment": "Perfect for my desk.",
            },
        )
        assert response.status_code == 401

    def test_create_duplicate_review_returns_409(self, client):
        headers = get_auth_header(client)
        client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 5,
                "title": "Great lamp!",
                "comment": "Perfect for my desk.",
            },
            headers=headers,
        )
        response = client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 4,
                "title": "Another review",
                "comment": "Trying to review again.",
            },
            headers=headers,
        )
        assert response.status_code == 409
        assert "already reviewed" in response.json()["detail"].lower()

    def test_create_review_invalid_rating_too_low(self, client):
        headers = get_auth_header(client)
        response = client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 0,
                "title": "Bad",
                "comment": "Rating too low.",
            },
            headers=headers,
        )
        assert response.status_code == 422

    def test_create_review_invalid_rating_too_high(self, client):
        headers = get_auth_header(client)
        response = client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 6,
                "title": "Bad",
                "comment": "Rating too high.",
            },
            headers=headers,
        )
        assert response.status_code == 422


class TestGetReviews:
    def test_get_reviews_for_product(self, client):
        headers = get_auth_header(client)
        client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 5,
                "title": "Great!",
                "comment": "Love it.",
            },
            headers=headers,
        )
        response = client.get("/api/reviews/desk-lamp")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["product_id"] == "desk-lamp"
        assert data[0]["rating"] == 5

    def test_get_reviews_empty_list(self, client):
        response = client.get("/api/reviews/nonexistent-product")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_reviews_ordered_by_newest(self, client):
        headers = get_auth_header(client, "user1@example.com", "StrongPass123")
        client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 4,
                "title": "First",
                "comment": "First review.",
            },
            headers=headers,
        )
        headers2 = get_auth_header(client, "user2@example.com", "StrongPass123")
        client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 5,
                "title": "Second",
                "comment": "Second review.",
            },
            headers=headers2,
        )
        response = client.get("/api/reviews/desk-lamp")
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Second"
        assert data[1]["title"] == "First"


class TestDeleteReview:
    def test_delete_own_review(self, client):
        headers = get_auth_header(client)
        create_resp = client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 5,
                "title": "Great!",
                "comment": "Love it.",
            },
            headers=headers,
        )
        review_id = create_resp.json()["id"]
        response = client.delete(f"/api/reviews/{review_id}", headers=headers)
        assert response.status_code == 204

    def test_delete_other_users_review_returns_403(self, client):
        headers1 = get_auth_header(client, "user1@example.com", "StrongPass123")
        create_resp = client.post(
            "/api/reviews",
            json={
                "product_id": "desk-lamp",
                "rating": 5,
                "title": "Great!",
                "comment": "Love it.",
            },
            headers=headers1,
        )
        review_id = create_resp.json()["id"]
        headers2 = get_auth_header(client, "user2@example.com", "StrongPass123")
        response = client.delete(f"/api/reviews/{review_id}", headers=headers2)
        assert response.status_code == 403
        assert "own reviews" in response.json()["detail"].lower()

    def test_delete_nonexistent_review_returns_404(self, client):
        headers = get_auth_header(client)
        response = client.delete("/api/reviews/99999", headers=headers)
        assert response.status_code == 404

    def test_delete_requires_auth(self, client):
        response = client.delete("/api/reviews/1")
        assert response.status_code == 401

# DevDesk Phase 1: Foundation — Design Spec

## Overview

Add foundational DevOps features to the DevDesk payment app: Docker Compose, GitHub Actions CI, Alembic migrations, and Rate Limiting.

## 1. Docker Compose

### Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `frontend` | Node 18 | 5173 | React dev server |
| `backend` | Python 3.11 | 8000 | FastAPI app |
| `db` | PostgreSQL 15 | 5432 | Database |
| `redis` | Redis 7 | 6379 | Cache (for future use) |

### Files

- `docker-compose.yml` — Service definitions
- `backend/Dockerfile` — Python app container
- `frontend/Dockerfile` — Node dev container
- `backend/.env.example` — Template for environment variables

### Usage

```bash
docker-compose up        # Start all services
docker-compose down      # Stop all services
docker-compose build     # Rebuild containers
```

### Environment Variables

The `.env` file is mounted into the backend container. No secrets in Dockerfile.

---

## 2. GitHub Actions CI

### Workflow

Triggers on: `push`, `pull_request` to `main`

### Jobs

| Job | Steps |
|-----|-------|
| `backend` | Install Python, install deps, run pytest |
| `frontend` | Install Node, install deps, run build, run lint |

### Files

- `.github/workflows/ci.yml`

### Behavior

- PR shows green check if all tests pass
- PR shows red X if any test fails
- No auto-deploy (CI only)

---

## 3. Alembic Migrations

### Setup

- Install `alembic` in backend
- Initialize Alembic in `backend/alembic/`
- Configure `alembic.ini` to use `DATABASE_URL` from env
- Generate initial migration from current schema
- Update `main.py` to use Alembic instead of `create_all()`

### Files

- `backend/alembic/` — Migration scripts
- `backend/alembic.ini` — Alembic config
- `backend/alembic/env.py` — Environment config
- `backend/app/database.py` — Update connection

### Commands

```bash
alembic upgrade head           # Apply all migrations
alembic downgrade -1           # Rollback one migration
alembic revision --autogenerate -m "description"  # Create new migration
```

### Initial Migration

Generate from current schema (User, Order, CartItem, Review, WishlistItem, Coupon, PasswordReset models).

---

## 4. Rate Limiting

### Library

`slowapi` — FastAPI-compatible rate limiter

### Limits

| Endpoint | Limit |
|----------|-------|
| `/api/auth/login` | 10 requests/minute per IP |
| `/api/auth/register` | 5 requests/minute per IP |
| `/api/auth/forgot-password` | 5 requests/minute per IP |
| All other endpoints | 120 requests/minute per IP |

### Response

When limit exceeded: `429 Too Many Requests` with message.

### Files

- `backend/app/middleware.py` — Rate limiter setup
- `backend/main.py` — Apply middleware

---

## Implementation Order

1. Docker Compose — local dev environment
2. Alembic — database migrations
3. Rate Limiting — auth protection
4. GitHub Actions CI — automated testing

## Success Criteria

- [ ] `docker-compose up` starts all services
- [ ] `alembic upgrade head` creates all tables
- [ ] `alembic revision --autogenerate` detects schema changes
- [ ] Rate limiting returns 429 on excessive requests
- [ ] GitHub Actions runs tests on push/PR
- [ ] All existing tests still pass

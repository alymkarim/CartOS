# Phase 1: Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Docker Compose, GitHub Actions CI, Alembic migrations, and Rate Limiting to the DevDesk payment app.

**Architecture:** Each feature is independent and can be implemented separately. Docker Compose provides local dev environment, Alembic replaces create_all() with versioned migrations, Rate Limiting protects auth endpoints, GitHub Actions runs tests automatically.

**Tech Stack:** Docker, Docker Compose, GitHub Actions, Alembic, slowapi, FastAPI, PostgreSQL, Redis

## Global Constraints

- Docker Compose uses PostgreSQL 15 and Redis 7
- Alembic migrations stored in `backend/alembic/`
- Rate limiting uses `slowapi` library
- GitHub Actions runs on push and pull_request to main
- All existing tests must continue to pass

---

## Branch Strategy

| Branch | Tasks | Description |
|---|---|---|
| `feature/docker-compose` | Task 1 | Docker Compose setup |
| `feature/alembic` | Task 2, 3 | Alembic setup and initial migration |
| `feature/rate-limiting` | Task 4 | Rate limiting on auth endpoints |
| `feature/github-actions` | Task 5 | GitHub Actions CI |

---

## Task 1: Docker Compose

**Branch:** `feature/docker-compose`

**Files:**
- Create: `docker-compose.yml`
- Create: `backend/Dockerfile`
- Create: `frontend/Dockerfile`
- Create: `backend/.env.example`

**Interfaces:**
- Produces: `docker-compose up` starts all services
- Consumes: Existing backend and frontend code

- [ ] **Step 1: Create backend Dockerfile**

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

- [ ] **Step 2: Create frontend Dockerfile**

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

- [ ] **Step 3: Create docker-compose.yml**

```yaml
# docker-compose.yml
version: "3.8"

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: devdesk
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/devdesk
      STRIPE_SECRET_KEY: ${STRIPE_SECRET_KEY}
      STRIPE_WEBHOOK_SECRET: ${STRIPE_WEBHOOK_SECRET}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      FRONTEND_URL: http://localhost:5173
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

- [ ] **Step 4: Create backend .env.example**

```bash
# backend/.env.example
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/devdesk
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_secret_here
JWT_SECRET_KEY=your_jwt_secret_here
FRONTEND_URL=http://localhost:5173
```

- [ ] **Step 5: Test Docker Compose**

```bash
docker-compose up --build
```

Verify:
- Frontend at http://localhost:5173
- Backend at http://localhost:8000
- PostgreSQL at localhost:5432
- Redis at localhost:6379

- [ ] **Step 6: Commit**

```bash
git add docker-compose.yml backend/Dockerfile frontend/Dockerfile backend/.env.example
git commit -m "add docker compose for local development"
```

---

## Task 2: Alembic Setup

**Branch:** `feature/alembic`

**Files:**
- Create: `backend/alembic/`
- Create: `backend/alembic.ini`
- Modify: `backend/requirements.txt`
- Modify: `backend/app/database.py`

**Interfaces:**
- Produces: `alembic` CLI, migration scripts
- Consumes: Existing SQLAlchemy models

- [ ] **Step 1: Install Alembic**

```bash
cd backend
pip install alembic
pip freeze > requirements.txt
```

- [ ] **Step 2: Initialize Alembic**

```bash
cd backend
alembic init alembic
```

- [ ] **Step 3: Configure alembic.ini**

Edit `backend/alembic.ini`:

```ini
# Line 62: change sqlalchemy.url
sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/devdesk
```

- [ ] **Step 4: Configure alembic/env.py**

Edit `backend/alembic/env.py`:

```python
# Add at top
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import models
from app.database import Base
from app import models

# Set target metadata
target_metadata = Base.metadata

# In run_migrations_online(), update connectable:
connectable = create_engine(os.getenv("DATABASE_URL"))
```

- [ ] **Step 5: Generate initial migration**

```bash
cd backend
alembic revision --autogenerate -m "initial schema"
```

- [ ] **Step 6: Apply migration**

```bash
cd backend
alembic upgrade head
```

- [ ] **Step 7: Update main.py to remove create_all**

Edit `backend/main.py`:

```python
# Remove or comment out:
# Base.metadata.create_all(bind=engine)
```

- [ ] **Step 8: Test migration**

```bash
cd backend
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

- [ ] **Step 9: Commit**

```bash
git add backend/alembic/ backend/alembic.ini backend/requirements.txt backend/app/database.py backend/main.py
git commit -m "add alembic for database migrations"
```

---

## Task 3: Alembic Initial Migration

**Branch:** `feature/alembic` (continued)

**Files:**
- Create: `backend/alembic/versions/` (initial migration)

**Interfaces:**
- Produces: Initial migration that creates all tables
- Consumes: All SQLAlchemy models

- [ ] **Step 1: Generate initial migration**

```bash
cd backend
alembic revision --autogenerate -m "create all tables"
```

- [ ] **Step 2: Review migration file**

Check the generated migration file in `backend/alembic/versions/` to ensure it creates all tables:
- users
- orders
- cart_items
- reviews
- wishlist_items
- coupons
- password_resets

- [ ] **Step 3: Apply migration**

```bash
cd backend
alembic upgrade head
```

- [ ] **Step 4: Verify tables exist**

```bash
# Connect to database and list tables
psql -h localhost -U postgres -d devdesk -c "\dt"
```

- [ ] **Step 5: Commit**

```bash
git add backend/alembic/versions/
git commit -m "add initial database migration"
```

---

## Task 4: Rate Limiting

**Branch:** `feature/rate-limiting`

**Files:**
- Create: `backend/app/middleware.py`
- Modify: `backend/main.py`
- Modify: `backend/requirements.txt`

**Interfaces:**
- Produces: Rate limiter middleware
- Consumes: `slowapi` library

- [ ] **Step 1: Install slowapi**

```bash
cd backend
pip install slowapi
pip freeze > requirements.txt
```

- [ ] **Step 2: Create middleware.py**

```python
# backend/app/middleware.py

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address)

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."},
    )
```

- [ ] **Step 3: Update main.py**

```python
# backend/main.py

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.middleware import limiter, rate_limit_exceeded_handler

# After creating app:
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
```

- [ ] **Step 4: Add rate limits to auth endpoints**

```python
# backend/app/routers/auth.py

from app.middleware import limiter

@router.post("/login")
@limiter.limit("10/minute")
def login(request: Request, ...):
    ...

@router.post("/register")
@limiter.limit("5/minute")
def register(request: Request, ...):
    ...

@router.post("/forgot-password")
@limiter.limit("5/minute")
def forgot_password(request: Request, ...):
    ...
```

- [ ] **Step 5: Test rate limiting**

```bash
# Send 11 requests quickly
for i in {1..11}; do
  curl -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test@test.com&password=test"
done
```

The 11th request should return 429.

- [ ] **Step 6: Commit**

```bash
git add backend/app/middleware.py backend/main.py backend/app/routers/auth.py backend/requirements.txt
git commit -m "add rate limiting on auth endpoints"
```

---

## Task 5: GitHub Actions CI

**Branch:** `feature/github-actions`

**Files:**
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Produces: CI workflow that runs on push/PR
- Consumes: Existing test suite

- [ ] **Step 1: Create CI workflow**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: devdesk_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/devdesk_test
          STRIPE_SECRET_KEY: sk_test_fake
          STRIPE_WEBHOOK_SECRET: whsec_fake
          JWT_SECRET_KEY: test-secret-key
          FRONTEND_URL: http://localhost:5173
        run: |
          cd backend
          python -m pytest

  frontend:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: "18"

      - name: Install dependencies
        run: |
          cd frontend
          npm install

      - name: Build
        run: |
          cd frontend
          npm run build

      - name: Lint
        run: |
          cd frontend
          npm run lint
```

- [ ] **Step 2: Test locally with act (optional)**

```bash
# Install act: brew install act
act -l  # List available jobs
act     # Run all jobs locally
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "add github actions ci workflow"
```

---

## Task 6: Final Integration Test

- [ ] **Step 1: Test Docker Compose**

```bash
docker-compose down -v
docker-compose up --build
```

Verify all services start.

- [ ] **Step 2: Test Alembic**

```bash
cd backend
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

- [ ] **Step 3: Test Rate Limiting**

```bash
# Send 11 requests quickly
for i in {1..11}; do
  curl -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test@test.com&password=test"
done
```

- [ ] **Step 4: Run all tests**

```bash
cd backend
python -m pytest
```

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "phase 1 foundation complete - docker, alembic, rate limiting, ci"
```

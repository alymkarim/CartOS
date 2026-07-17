# 💳 CartOS

A modern full-stack payment platform built with **FastAPI, React, PostgreSQL, Stripe, JWT Authentication, and Docker**.

CartOS demonstrates how a production-style payment system is designed, from secure authentication and REST APIs to payment processing, database persistence, and cloud deployment.

> **Status:** 🚧 Active Development

---

# 🚀 Overview

CartOS is a full-stack e-commerce and payment application designed to showcase modern backend and frontend software engineering practices.

The application allows users to browse products, complete payments through Stripe Checkout, and stores successful purchases in a PostgreSQL database. The backend follows a modular architecture using FastAPI, while the frontend is built with React and TypeScript.

The project is being developed incrementally to reflect how production systems evolve, with authentication, authorization, testing, deployment, and monitoring added over time.

---

# ✨ Current Features

## Backend

- REST API built with FastAPI
- PostgreSQL database (Supabase)
- SQLAlchemy ORM
- Pydantic validation
- Modular router architecture
- Environment variable configuration
- Health check endpoint
- CORS configuration
- Product API
- Order API
- Stripe Checkout integration
- Stripe Webhook integration
- Payment persistence
- JWT Authentication
- Password hashing
- User registration
- User login
- Protected API endpoints
- User database relationships

---

## Frontend

- React + TypeScript
- Product catalogue
- Stripe Checkout integration
- Orders page
- API communication with FastAPI
- Responsive layout (in progress)

---

## Payments

- Secure Stripe Checkout
- Webhook signature verification
- Automatic order creation after successful payment
- PostgreSQL order storage

---

# 🛠 Tech Stack

### Frontend

- React
- TypeScript
- Vite
- CSS

### Backend

- FastAPI
- SQLAlchemy 2.0
- Pydantic
- Uvicorn

### Database

- PostgreSQL
- Supabase

### Authentication

- JWT
- Argon2 Password Hashing

### Payments

- Stripe Checkout
- Stripe Webhooks

### Development

- Git
- GitHub
- Docker (in progress)
- Postman
- Swagger UI

---

# 📁 Project Structure

```text
payment-app/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── backend/
│   ├── app/
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── checkout.py
│   │   ├── webhook.py
│   │   └── orders.py
│   │
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── security.py
│   ├── dependencies.py
│   └── config.py
│
└── README.md
```

---

# 🧱 Architecture

```
React Frontend
        │
        ▼
 FastAPI REST API
        │
        ▼
 Authentication (JWT)
        │
        ▼
 Business Logic
        │
        ▼
 Stripe Checkout
        │
        ▼
 Stripe Webhooks
        │
        ▼
 PostgreSQL (Supabase)
```

---

# 🔐 Authentication

Current implementation includes:

- User Registration
- User Login
- Password Hashing
- JWT Access Tokens
- Protected API Endpoints

Authentication is being expanded to support production-style security practices.

---

# 💳 Payment Flow

```
User selects product
        │
        ▼
Checkout API
        │
        ▼
Stripe Checkout
        │
        ▼
Payment Success
        │
        ▼
Stripe Webhook
        │
        ▼
Order stored in PostgreSQL
```

---

# 📸 Screenshots

### Home Page

<img src="images/home.png">

### Products

<img src="images/products.png">

### Checkout

<img src="images/checkout.png">

### Orders

<img src="images/orders.png">

---

# 🧪 Testing

Current testing includes:

- API testing using Swagger UI
- Endpoint validation
- Database integration testing
- Stripe test payments

Planned:

- Unit Tests
- Integration Tests
- Authentication Tests
- Webhook Tests

---

# 🚀 Deployment

| Service | Platform |
|----------|----------|
| Frontend | Vercel *(planned)* |
| Backend | Render *(planned)* |
| Database | Supabase |
| Payments | Stripe |

---

# 📈 Roadmap

## Authentication

- [x] User Registration
- [x] User Login
- [x] JWT Authentication
- [ ] Refresh Tokens
- [ ] Email Verification
- [ ] Password Reset
- [ ] Role-Based Authorization

---

## Payments

- [x] Stripe Checkout
- [x] Stripe Webhooks
- [x] Order Storage
- [ ] User-linked Orders
- [ ] Refund Support
- [ ] Order Status Management

---

## Frontend

- [x] Product Catalogue
- [x] Checkout
- [x] Orders Page
- [ ] Login Page
- [ ] Register Page
- [ ] User Dashboard
- [ ] Admin Dashboard

---

## Backend

- [x] FastAPI
- [x] PostgreSQL
- [x] SQLAlchemy
- [ ] Alembic Migrations
- [ ] Redis Caching
- [ ] Background Jobs
- [ ] Structured Logging
- [ ] Monitoring
- [ ] Rate Limiting

---

## DevOps

- [ ] Docker Compose
- [ ] CI/CD (GitHub Actions)
- [ ] Production Deployment
- [ ] Automated Testing Pipeline

---

# 🎯 Learning Objectives

This project is being developed to strengthen practical software engineering skills including:

- Backend API Development
- Authentication & Authorization
- Payment Processing
- Database Design
- Software Architecture
- Testing
- Deployment
- Production Engineering Practices
- Secure Application Development

---

# 📄 License

This project is intended for educational and portfolio purposes.

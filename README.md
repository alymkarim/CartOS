# DevDesk

> Previously known as CartOS. Renamed to DevDesk because the store sells developer workspace gear, not generic carts.

A full-stack e-commerce store for developer workspace gear, built with FastAPI, React, PostgreSQL, and Stripe.

---

## Why DevDesk?

The original name "CartOS" was generic and didn't reflect what the store actually sells — premium gear for developers who care about their workspace. DevDesk is clearer, more memorable, and fits the product theme.

---

## Features

### Core
- Product catalog with 8 developer workspace products (keyboards, monitors, headsets, etc.)
- Stripe Checkout integration (test mode)
- Shopping cart with guest (localStorage) and logged-in (API) support
- User authentication (register, login, password reset)
- JWT-based session management
- Responsive design with Tailwind CSS

### E-Commerce
- Product reviews with star ratings (1-5) and text comments
- Wishlist with heart icon toggle and dedicated page
- Order tracking with 4-step timeline (pending → processing → shipped → delivered)
- Discount codes (percentage and fixed amount)
- User-scoped order history

### UI/UX
- Landing page with hero section and featured products
- Product catalog with search
- Product detail pages with quantity selector
- Cart page with order summary and coupon input
- Account page with profile and order history
- Mobile hamburger menu
- Error boundary and loading states

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7 |
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic |
| Database | PostgreSQL (Supabase) |
| Auth | JWT, Argon2 password hashing |
| Payments | Stripe Checkout, Stripe Webhooks |
| Hosting | Vercel (frontend), Render (backend) |

---

## How It Was Built

This project was built incrementally, starting from a basic FastAPI + React setup and adding features over time:

1. **Backend setup** — FastAPI, SQLAlchemy, PostgreSQL connection
2. **Product API** — Hardcoded product catalog with 8 items
3. **Stripe integration** — Checkout sessions and webhook handling
4. **Frontend foundation** — React + TypeScript + Vite + Tailwind CSS
5. **Auth system** — JWT login/register, password reset, protected routes
6. **Cart system** — Guest cart (localStorage) + logged-in cart (API)
7. **Product reviews** — Star ratings, text reviews, average rating display
8. **Wishlist** — Heart icon toggle, dedicated wishlist page
9. **Order tracking** — 4-step timeline with status badges
10. **Discount codes** — Coupon validation and checkout integration

Each feature was built on a separate branch and merged to main, following a clean Git workflow.

---

## Project Structure

```
├── frontend/                  # React + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── layout/        # Navbar, Footer, ProtectedRoute
│   │   │   └── ui/            # Button, Input, Spinner, Badge
│   │   ├── contexts/          # AuthContext, CartContext
│   │   ├── pages/             # All page components
│   │   ├── services/          # API client
│   │   └── types/             # TypeScript interfaces
│   ├── vercel.json
│   └── package.json
│
├── backend/                   # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── routers/           # API endpoints
│   │   │   ├── auth.py        # Register, login, password reset
│   │   │   ├── cart.py        # Cart CRUD
│   │   │   ├── checkout.py    # Stripe checkout
│   │   │   ├── coupons.py     # Discount code validation
│   │   │   ├── orders.py      # Order history + tracking
│   │   │   ├── products.py    # Product catalog
│   │   │   ├── reviews.py     # Product reviews
│   │   │   ├── webhook.py     # Stripe webhook handler
│   │   │   └── wishlist.py    # Wishlist CRUD
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── security.py        # Password hashing, JWT
│   │   └── config.py          # Environment variables
│   ├── tests/                 # Pytest test suite
│   └── requirements.txt
│
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database (or Supabase)
- Stripe account (test mode)

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your credentials
python -m uvicorn main:app --reload
```

API runs at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at http://localhost:5173

### Environment Variables

Create `backend/.env`:

```
DATABASE_URL=postgresql://user:pass@host:5432/db
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=http://localhost:5173
```

---

## Docker

**Status: Not implemented yet.**

Planned:
- `docker-compose.yml` for frontend + backend + PostgreSQL
- Dockerfile for backend (Python)
- Dockerfile for frontend (Node + Nginx)
- Environment variable injection

---

## Deployment

| Service | Platform | Status |
|---------|----------|--------|
| Frontend | Vercel | Ready to deploy |
| Backend | Render | Ready to deploy |
| Database | Supabase | Active |
| Payments | Stripe | Test mode |

---

## Future Improvements

### Features
- [ ] Admin dashboard (manage products, view orders, revenue charts)
- [ ] Product categories and filtering
- [ ] Search autocomplete
- [ ] Recently viewed products
- [ ] Related products ("You might also like")
- [ ] Order confirmation emails
- [ ] User profile editing (change email, password)
- [ ] Social login (Google, GitHub OAuth)

### Technical
- [ ] Docker Compose setup
- [ ] CI/CD with GitHub Actions
- [ ] Alembic database migrations
- [ ] Redis caching for product catalog
- [ ] Rate limiting on auth endpoints
- [ ] Structured logging
- [ ] Monitoring and alerting
- [ ] Automated test pipeline

### Payments
- [ ] Refund support
- [ ] Subscription payments
- [ ] Multiple payment methods
- [ ] Invoice generation

---

## Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend build check
cd frontend
npm run build
```

Current test coverage: 62 tests passing (auth, reviews, wishlist, orders, coupons)

---

## License

Portfolio project. Built for educational purposes.

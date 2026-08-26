# DevDesk

A full-stack e-commerce store for developer workspace gear, built with FastAPI, React, PostgreSQL, and Stripe.

## Live Demo

- **Frontend:** https://dev-desk-nine.vercel.app
- **Backend API:** https://devdesk-1.onrender.com
- **API Docs:** https://devdesk-1.onrender.com/docs

## Features

### Store
- 12 developer workspace products with real images
- Product detail pages with quantity selector
- Product search and filtering
- Product reviews with star ratings (1-5)
- Wishlist with heart icon toggle

### Shopping
- Shopping cart with guest (localStorage) and logged-in (API) support
- Discount codes (percentage and fixed amount)
- Stripe Checkout integration (test mode)
- Order confirmation via webhook

### User Accounts
- Registration with password strength meter
- Login with JWT authentication
- Password reset flow
- Order history with status tracking
- 4-step order timeline (pending, processing, shipped, delivered)

### Technical
- Responsive design with Tailwind CSS
- Mobile hamburger navigation
- Rate limiting on auth endpoints
- Alembic database migrations
- Docker Compose for local development
- GitHub Actions CI (tests + lint)
- Error boundary for graceful error handling

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7 |
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic, Alembic |
| Database | PostgreSQL (Supabase) |
| Auth | JWT, Argon2 password hashing |
| Payments | Stripe Checkout, Stripe Webhooks |
| DevOps | Docker, GitHub Actions, Vercel, Render |

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL (or Supabase)
- Stripe account (test mode)

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # Add your credentials
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

### Docker Compose

```bash
docker-compose up --build
```

Starts frontend, backend, PostgreSQL, and Redis.

### Environment Variables

Create `backend/.env`:

```
DATABASE_URL=postgresql://user:pass@host:5432/db
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=http://localhost:5173
```

## Project Structure

```
├── frontend/                  # React + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── contexts/          # AuthContext, CartContext
│   │   ├── pages/             # All page components
│   │   ├── services/          # API client
│   │   └── types/             # TypeScript interfaces
│   └── package.json
│
├── backend/                   # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── routers/           # API endpoints
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── security.py        # Password hashing, JWT
│   │   └── config.py          # Environment variables
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Pytest test suite
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/products | List all products |
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login |
| POST | /api/auth/forgot-password | Request password reset |
| POST | /api/auth/reset-password | Reset password |
| GET | /api/cart | Get cart items |
| POST | /api/cart | Add to cart |
| DELETE | /api/cart/{id} | Remove from cart |
| POST | /api/checkout/cart | Checkout cart via Stripe |
| GET | /api/orders | Get user orders |
| GET | /api/orders/{id} | Get order detail |
| GET | /api/reviews/{product_id} | Get product reviews |
| POST | /api/reviews | Create review |
| GET | /api/wishlist | Get wishlist |
| POST | /api/wishlist/{product_id} | Add to wishlist |
| POST | /api/coupons/validate | Validate discount code |

## Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend build check
cd frontend
npm run build
npm run lint
```

65 tests passing across auth, coupons, orders, reviews, wishlist, and rate limiting.

## Deployment

| Service | Platform | Status |
|---------|----------|--------|
| Frontend | Vercel | Live |
| Backend | Render | Live |
| Database | Supabase | Active |
| Payments | Stripe | Test mode |

## Future Improvements

- Admin dashboard for product and order management
- Product categories and advanced filtering
- Email notifications for order updates
- Refund processing through Stripe
- Subscription payments
- Invoice PDF generation
- Redis caching for product catalog
- Structured logging and monitoring

## License

Portfolio project.

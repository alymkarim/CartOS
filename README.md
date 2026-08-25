# DevDesk

A full-stack e-commerce store for developer workspace gear, built with FastAPI, React, PostgreSQL, and Stripe.

## Features

- Product catalog with 8 developer workspace products
- User authentication (register, login, password reset)
- Shopping cart with guest and logged-in support
- Stripe Checkout integration
- Product reviews with star ratings
- Wishlist with heart icon toggle
- Order tracking with 4-step timeline
- Discount codes (percentage and fixed amount)
- Responsive design with Tailwind CSS

## Tech Stack

**Frontend:** React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7

**Backend:** FastAPI, SQLAlchemy, PostgreSQL, Stripe

**Auth:** JWT with password hashing (Argon2)

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Environment Variables

Create `backend/.env`:

```
DATABASE_URL=postgresql://...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
JWT_SECRET_KEY=your-secret-key
FRONTEND_URL=http://localhost:5173
```

## Deployment

| Service | Platform |
|---------|----------|
| Frontend | Vercel |
| Backend | Render |
| Database | Supabase |
| Payments | Stripe |

## Project Structure

```
├── frontend/          # React + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
│
├── backend/           # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── routers/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── security.py
│   └── requirements.txt
│
└── README.md
```

## License

Portfolio project.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.middleware import limiter, rate_limit_exceeded_handler
from app.routers import auth, cart, checkout, coupons, orders, products, reviews, webhook, wishlist

settings = get_settings()

app = FastAPI(title="DevDesk API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# CORS - allow frontend URL from env + localhost for dev
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
if settings.frontend_url:
    allowed_origins.append(settings.frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(checkout.router)
app.include_router(webhook.router)
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(cart.router)
app.include_router(reviews.router)
app.include_router(wishlist.router)
app.include_router(coupons.router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "PayFlow API is running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
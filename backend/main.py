from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import checkout, products, webhook


settings = get_settings()

app = FastAPI(
    title="PayFlow API",
    description="FastAPI and Stripe Checkout payment API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


app.include_router(products.router)
app.include_router(checkout.router)
app.include_router(webhook.router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "PayFlow API is running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str
    name: str
    description: str
    price_cents: int = Field(gt=0)
    currency: str = "eur"
    emoji: str


class CheckoutRequest(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=10)


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str
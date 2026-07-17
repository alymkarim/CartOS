from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class OrderOut(BaseModel):
    id: int
    stripe_session_id: str
    product_id: str
    quantity: int
    payment_status: str
    amount_total: int | None
    customer_email: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


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
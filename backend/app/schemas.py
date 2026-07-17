from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str
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
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
    status: str
    status_updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Product(BaseModel):
    id: str
    name: str
    description: str
    price_cents: int = Field(gt=0)
    currency: str = "eur"
    emoji: str
    image_url: str


class CheckoutRequest(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=10)


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=10)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1, le=10)


class CartItemOut(BaseModel):
    id: int
    product_id: str
    quantity: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    token: str
    message: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str = Field(min_length=8, max_length=128)


class ReviewCreate(BaseModel):
    product_id: str
    rating: int = Field(ge=1, le=5)
    title: str = Field(max_length=100)
    comment: str = Field(max_length=1000)


class ReviewOut(BaseModel):
    id: int
    user_id: int
    product_id: str
    rating: int
    title: str
    comment: str
    created_at: datetime
    user_email: str

    model_config = ConfigDict(from_attributes=True)


class WishlistItemOut(BaseModel):
    id: int
    product_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
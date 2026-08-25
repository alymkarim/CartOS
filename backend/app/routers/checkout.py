import stripe
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Coupon, User
from app.product import get_product
from app.schemas import CheckoutRequest, CheckoutResponse


router = APIRouter(
    prefix="/api/checkout",
    tags=["Checkout"],
)


class CartCheckoutRequest(BaseModel):
    items: list[CheckoutRequest]
    coupon_code: str | None = None


@router.post(
    "/session",
    response_model=CheckoutResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_checkout_session(
    checkout_request: CheckoutRequest,
    settings: Settings = Depends(get_settings),
) -> CheckoutResponse:

    product = get_product(checkout_request.product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    if not settings.stripe_secret_key.startswith("sk_test_"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe test key is not configured correctly.",
        )

    stripe.api_key = settings.stripe_secret_key

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": product.currency,
                        "product_data": {
                            "name": product.name,
                            "description": product.description,
                        },
                        "unit_amount": product.price_cents,
                    },
                    "quantity": checkout_request.quantity,
                }
            ],
            success_url=(
                f"{settings.frontend_url}/checkout/success"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=f"{settings.frontend_url}/checkout/cancel",
            metadata={
                "product_id": product.id,
                "quantity": str(checkout_request.quantity),
            },
        )

    except stripe.StripeError as error:
        print("STRIPE ERROR:", str(error))

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    if not session.url:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Stripe did not return a checkout URL.",
        )

    return CheckoutResponse(
        checkout_url=session.url,
        session_id=session.id,
    )


@router.post(
    "/cart",
    response_model=CheckoutResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cart_checkout_session(
    checkout_request: CartCheckoutRequest,
    settings: Settings = Depends(get_settings),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CheckoutResponse:
    if not settings.stripe_secret_key.startswith("sk_test_"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe test key is not configured correctly.",
        )

    stripe.api_key = settings.stripe_secret_key

    line_items = []
    product_ids = []
    for item in checkout_request.items:
        product = get_product(item.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found.",
            )
        line_items.append({
            "price_data": {
                "currency": product.currency,
                "product_data": {
                    "name": product.name,
                    "description": product.description,
                },
                "unit_amount": product.price_cents,
            },
            "quantity": item.quantity,
        })
        product_ids.append(f"{product.id}:{item.quantity}")

    discount_amount = 0
    coupon = None
    if checkout_request.coupon_code:
        coupon = (
            db.query(Coupon)
            .filter(Coupon.code == checkout_request.coupon_code.upper())
            .first()
        )
        if not coupon:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid coupon code.",
            )
        if not coupon.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This coupon is no longer active.",
            )
        now = datetime.now(timezone.utc)
        expires_at = coupon.expires_at
        if expires_at and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at and expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This coupon has expired.",
            )
        if coupon.max_uses is not None and coupon.uses_count >= coupon.max_uses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This coupon has reached its usage limit.",
            )
        total_amount = 0
        for item in checkout_request.items:
            product_for_total = get_product(item.product_id)
            if product_for_total:
                total_amount += product_for_total.price_cents * item.quantity
        if coupon.min_order_amount and total_amount < coupon.min_order_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Minimum order amount is €{coupon.min_order_amount / 100:.2f}.",
            )
        if coupon.discount_type == "percentage":
            discount_amount = int(total_amount * coupon.discount_value / 100)
        else:
            discount_amount = min(coupon.discount_value, total_amount)

    try:
        session_params = {
            "mode": "payment",
            "line_items": line_items,
            "success_url": (
                f"{settings.frontend_url}/checkout/success"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),
            "cancel_url": f"{settings.frontend_url}/checkout/cancel",
            "metadata": {
                "user_id": str(current_user.id),
                "cart_checkout": "true",
                "items": "|".join(product_ids),
            },
        }
        if discount_amount > 0:
            session_params["discounts"] = [
                {
                    "coupon": stripe.Coupon.create(
                        amount_off=discount_amount,
                        currency="eur",
                        duration="once",
                    ),
                }
            ]
        session = stripe.checkout.Session.create(**session_params)
    except stripe.StripeError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    if not session.url:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Stripe did not return a checkout URL.",
        )

    return CheckoutResponse(
        checkout_url=session.url,
        session_id=session.id,
    )
import stripe
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.dependencies import get_current_user
from app.models import User
from app.product import get_product
from app.schemas import CheckoutRequest, CheckoutResponse


router = APIRouter(
    prefix="/api/checkout",
    tags=["Checkout"],
)


class CartCheckoutRequest(BaseModel):
    items: list[CheckoutRequest]


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
) -> CheckoutResponse:
    if not settings.stripe_secret_key.startswith("sk_test_"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe test key is not configured correctly.",
        )

    line_items = []
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

    stripe.api_key = settings.stripe_secret_key

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=(
                f"{settings.frontend_url}/checkout/success"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=f"{settings.frontend_url}/checkout/cancel",
            metadata={
                "user_id": str(current_user.id),
                "cart_checkout": "true",
            },
        )
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
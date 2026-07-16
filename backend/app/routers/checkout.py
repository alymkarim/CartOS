import stripe
from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.products import get_product
from app.schemas import CheckoutRequest, CheckoutResponse


router = APIRouter(
    prefix="/api/checkout",
    tags=["Checkout"],
)


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
                f"{settings.frontend_url}/success"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=f"{settings.frontend_url}/cancel",
            metadata={
                "product_id": product.id,
                "quantity": str(checkout_request.quantity),
            },
        )

    except stripe.StripeError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Stripe could not create the checkout session.",
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
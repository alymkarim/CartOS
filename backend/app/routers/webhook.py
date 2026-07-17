import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.config import Settings, get_settings


router = APIRouter(
    prefix="/api/webhooks",
    tags=["Webhooks"],
)


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe signature.",
        )

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=signature,
            secret=settings.stripe_webhook_secret,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook payload.",
        ) from error

    except stripe.SignatureVerificationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature.",
        ) from error

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        print("PAYMENT COMPLETED")
        print("Session ID:", session["id"])
        print("Payment status:", session.get("payment_status"))
        print("Product ID:", session.get("metadata", {}).get("product_id"))
        print("Quantity:", session.get("metadata", {}).get("quantity"))

    return {"received": True}
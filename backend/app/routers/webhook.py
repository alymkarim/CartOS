import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.models import Order

router = APIRouter(
    prefix="/api/webhooks",
    tags=["Webhooks"],
)


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
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
    
    if event.type == "checkout.session.completed":
        checkout_session = event.data.object
        metadata = checkout_session.metadata

        stripe_session_id = checkout_session.id
        product_id = metadata.product_id
        quantity = int(metadata.quantity)

        existing_order = (
            db.query(Order)
            .filter(Order.stripe_session_id == stripe_session_id)
            .first()
    )

    if existing_order:
        print("Order already exists:", stripe_session_id)
        return {
            "received": True,
            "message": "Order already processed",
        }

    customer_email = None

    if checkout_session.customer_details:
        customer_email = checkout_session.customer_details.email

    new_order = Order(
        stripe_session_id=stripe_session_id,
        product_id=product_id,
        quantity=quantity,
        payment_status=checkout_session.payment_status,
        amount_total=checkout_session.amount_total,
        customer_email=customer_email,
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

    except Exception:
        db.rollback()
        raise

    print("ORDER SAVED")
    print("Order ID:", new_order.id)
    print("Stripe session:", new_order.stripe_session_id)
    print("Product:", new_order.product_id)
    print("Quantity:", new_order.quantity)
    print("Amount:", new_order.amount_total)

    return {"received": True}
from datetime import datetime, timezone

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

        user_id = None
        if metadata.get("user_id"):
            user_id = int(metadata.user_id)

        # Handle cart checkout (multiple items)
        if metadata.get("cart_checkout") == "true":
            stripe.api_key = settings.stripe_secret_key
            line_items = stripe.checkout.Session.list_line_items(stripe_session_id, limit=100)
            
            for item in line_items.data:
                product_name = item.description or "Unknown Product"
                # Try to find product_id from price metadata
                product_id = "unknown"
                if item.price and item.price.product:
                    # Get product from Stripe to check metadata
                    try:
                        stripe_product = stripe.Product.retrieve(item.price.product)
                        if stripe_product.metadata and stripe_product.metadata.get("product_id"):
                            product_id = stripe_product.metadata.get("product_id")
                    except Exception:
                        pass
                
                new_order = Order(
                    stripe_session_id=stripe_session_id,
                    product_id=product_id,
                    quantity=item.quantity,
                    payment_status=checkout_session.payment_status,
                    amount_total=item.amount_total,
                    customer_email=customer_email,
                    user_id=user_id,
                    status="pending",
                    status_updated_at=datetime.now(timezone.utc),
                )
                db.add(new_order)
            
            try:
                db.commit()
                print("CART ORDER SAVED:", stripe_session_id)
            except Exception:
                db.rollback()
                raise
        else:
            # Handle single product checkout
            product_id = metadata.product_id
            quantity = int(metadata.quantity)

            new_order = Order(
                stripe_session_id=stripe_session_id,
                product_id=product_id,
                quantity=quantity,
                payment_status=checkout_session.payment_status,
                amount_total=checkout_session.amount_total,
                customer_email=customer_email,
                user_id=user_id,
                status="pending",
                status_updated_at=datetime.now(timezone.utc),
            )

            try:
                db.add(new_order)
                db.commit()
                db.refresh(new_order)
                print("ORDER SAVED:", new_order.id)
            except Exception:
                db.rollback()
                raise

    return {"received": True}
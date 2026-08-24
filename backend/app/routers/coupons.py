from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Coupon, User
from app.schemas import CouponValidate, CouponValidationResponse

router = APIRouter(
    prefix="/api/coupons",
    tags=["Coupons"],
)


@router.post("/validate", response_model=CouponValidationResponse)
def validate_coupon(
    request: CouponValidate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    coupon = (
        db.query(Coupon)
        .filter(Coupon.code == request.code.upper())
        .first()
    )

    if not coupon:
        return CouponValidationResponse(
            valid=False,
            discount_amount=0,
            message="Invalid coupon code.",
        )

    if not coupon.is_active:
        return CouponValidationResponse(
            valid=False,
            discount_amount=0,
            message="This coupon is no longer active.",
        )

    now = datetime.now(timezone.utc)
    expires_at = coupon.expires_at
    if expires_at and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at and expires_at < now:
        return CouponValidationResponse(
            valid=False,
            discount_amount=0,
            message="This coupon has expired.",
        )

    if coupon.max_uses is not None and coupon.uses_count >= coupon.max_uses:
        return CouponValidationResponse(
            valid=False,
            discount_amount=0,
            message="This coupon has reached its usage limit.",
        )

    if coupon.min_order_amount and request.order_amount < coupon.min_order_amount:
        return CouponValidationResponse(
            valid=False,
            discount_amount=0,
            message=f"Minimum order amount is €{coupon.min_order_amount / 100:.2f}.",
        )

    if coupon.discount_type == "percentage":
        discount = int(request.order_amount * coupon.discount_value / 100)
    else:
        discount = min(coupon.discount_value, request.order_amount)

    return CouponValidationResponse(
        valid=True,
        discount_amount=discount,
        message=f"Coupon applied! You save €{discount / 100:.2f}.",
    )

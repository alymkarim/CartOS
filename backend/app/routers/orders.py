from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order
from app.schemas import OrderOut


router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"],
)


@router.get("", response_model=list[OrderOut])
def get_orders(
    db: Session = Depends(get_db),
):
    return (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .all()
    )
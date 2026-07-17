from fastapi import APIRouter

from app.product import list_products
from app.schemas import Product


router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


@router.get("", response_model=list[Product])
def read_products() -> list[Product]:
    return list_products()
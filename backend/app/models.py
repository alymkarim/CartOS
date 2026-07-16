from app.schemas import Product


PRODUCTS: dict[str, Product] = {
    "desk-lamp": Product(
        id="desk-lamp",
        name="Focus Desk Lamp",
        description="A compact lamp for a clean and focused workspace.",
        price_cents=2999,
        currency="eur",
        emoji="💡",
    ),
    "mechanical-keyboard": Product(
        id="mechanical-keyboard",
        name="Mechanical Keyboard",
        description="A tactile keyboard for coding and everyday work.",
        price_cents=7999,
        currency="eur",
        emoji="⌨️",
    ),
    "developer-mug": Product(
        id="developer-mug",
        name="Developer Mug",
        description="A ceramic mug for coffee-powered debugging sessions.",
        price_cents=1499,
        currency="eur",
        emoji="☕",
    ),
}


def list_products() -> list[Product]:
    return list(PRODUCTS.values())


def get_product(product_id: str) -> Product | None:
    return PRODUCTS.get(product_id)
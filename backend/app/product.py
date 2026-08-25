from app.schemas import Product

PRODUCTS: dict[str, Product] = {
    "desk-lamp": Product(
        id="desk-lamp",
        name="Focus Desk Lamp",
        description="Adjustable LED lamp with warm and cool color temperature modes. Perfect for late-night coding sessions.",
        price_cents=2999,
        currency="eur",
        emoji="💡",
        image_url="https://images.unsplash.com/photo-1621177555452-bedbe4c28879?w=800&h=800&fit=crop",
    ),
    "mechanical-keyboard": Product(
        id="mechanical-keyboard",
        name="MX Artisan Keyboard",
        description="Hot-swappable mechanical keyboard with PBT keycaps and per-key RGB lighting. Tactile switches included.",
        price_cents=7999,
        currency="eur",
        emoji="⌨️",
        image_url="https://images.unsplash.com/photo-1711638244036-9ed8ecdef324?w=800&h=800&fit=crop",
    ),
    "developer-mug": Product(
        id="developer-mug",
        name="Debug Fuel Mug",
        description="12oz ceramic mug with a matte finish. Dishwasher and microwave safe. Holds enough coffee for a sprint.",
        price_cents=1499,
        currency="eur",
        emoji="☕",
        image_url="https://images.unsplash.com/photo-1495100497150-fe209c585f50?w=800&h=800&fit=crop",
    ),
    "ultrawide-monitor": Product(
        id="ultrawide-monitor",
        name='UltraWide 34"',
        description="3440x1440 curved IPS display with USB-C power delivery. 100Hz refresh rate, HDR400.",
        price_cents=44999,
        currency="eur",
        emoji="🖥️",
        image_url="https://images.unsplash.com/photo-1674083401439-e358eda52589?w=800&h=800&fit=crop",
    ),
    "webcam-pro": Product(
        id="webcam-pro",
        name="StreamCam Pro",
        description="4K webcam with auto-light correction and noise-cancelling dual microphones. USB-C connection.",
        price_cents=8999,
        currency="eur",
        emoji="📷",
        image_url="https://images.unsplash.com/photo-1650017069617-61720acdd884?w=800&h=800&fit=crop",
    ),
    "desk-mat": Product(
        id="desk-mat",
        name="Felt Desk Mat",
        description="Premium wool felt desk mat, 900x400mm. Includes genuine leather strap for easy rolling and storage.",
        price_cents=3499,
        currency="eur",
        emoji="🖱️",
        image_url="https://images.unsplash.com/photo-1706615737134-a7778e037715?w=800&h=800&fit=crop",
    ),
    "noise-cancelling": Product(
        id="noise-cancelling",
        name="QuietPro Headset",
        description="Active noise cancelling over-ear headphones with 40-hour battery life. Multipoint Bluetooth connectivity.",
        price_cents=19999,
        currency="eur",
        emoji="🎧",
        image_url="https://images.unsplash.com/photo-1576082712237-eb1335ce23a3?w=800&h=800&fit=crop",
    ),
    "usb-c-hub": Product(
        id="usb-c-hub",
        name="Thunderbolt Hub",
        description="7-in-1 USB-C hub with dual HDMI 4K output, 100W power delivery, and gigabit ethernet.",
        price_cents=6999,
        currency="eur",
        emoji="🔌",
        image_url="https://images.unsplash.com/photo-1760376789478-c1023d2dc007?w=800&h=800&fit=crop",
    ),
}


def list_products() -> list[Product]:
    return list(PRODUCTS.values())


def get_product(product_id: str) -> Product | None:
    return PRODUCTS.get(product_id)

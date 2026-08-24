from app.schemas import Product

PRODUCTS: dict[str, Product] = {
    "desk-lamp": Product(
        id="desk-lamp",
        name="Focus Desk Lamp",
        description="Adjustable LED lamp with warm and cool color temperature modes. Perfect for late-night coding sessions.",
        price_cents=2999,
        currency="eur",
        emoji="💡",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=400&h=400&fit=crop",
    ),
    "mechanical-keyboard": Product(
        id="mechanical-keyboard",
        name="MX Artisan Keyboard",
        description="Hot-swappable mechanical keyboard with PBT keycaps and per-key RGB lighting. Tactile switches included.",
        price_cents=7999,
        currency="eur",
        emoji="⌨️",
        image_url="https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=400&fit=crop",
    ),
    "developer-mug": Product(
        id="developer-mug",
        name="Debug Fuel Mug",
        description="12oz ceramic mug with a matte finish. Dishwasher and microwave safe. Holds enough coffee for a sprint.",
        price_cents=1499,
        currency="eur",
        emoji="☕",
        image_url="https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&h=400&fit=crop",
    ),
    "ultrawide-monitor": Product(
        id="ultrawide-monitor",
        name='UltraWide 34"',
        description="3440x1440 curved IPS display with USB-C power delivery. 100Hz refresh rate, HDR400.",
        price_cents=44999,
        currency="eur",
        emoji="🖥️",
        image_url="https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop",
    ),
    "webcam-pro": Product(
        id="webcam-pro",
        name="StreamCam Pro",
        description="4K webcam with auto-light correction and noise-cancelling dual microphones. USB-C connection.",
        price_cents=8999,
        currency="eur",
        emoji="📷",
        image_url="https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400&h=400&fit=crop",
    ),
    "desk-mat": Product(
        id="desk-mat",
        name="Felt Desk Mat",
        description="Premium wool felt desk mat, 900x400mm. Includes genuine leather strap for easy rolling and storage.",
        price_cents=3499,
        currency="eur",
        emoji="🖱️",
        image_url="https://images.unsplash.com/photo-1616628188540-925618b4c45a?w=400&h=400&fit=crop",
    ),
    "noise-cancelling": Product(
        id="noise-cancelling",
        name="QuietPro Headset",
        description="Active noise cancelling over-ear headphones with 40-hour battery life. Multipoint Bluetooth connectivity.",
        price_cents=19999,
        currency="eur",
        emoji="🎧",
        image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
    ),
    "usb-c-hub": Product(
        id="usb-c-hub",
        name="Thunderbolt Hub",
        description="7-in-1 USB-C hub with dual HDMI 4K output, 100W power delivery, and gigabit ethernet.",
        price_cents=6999,
        currency="eur",
        emoji="🔌",
        image_url="https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400&h=400&fit=crop",
    ),
}


def list_products() -> list[Product]:
    return list(PRODUCTS.values())


def get_product(product_id: str) -> Product | None:
    return PRODUCTS.get(product_id)

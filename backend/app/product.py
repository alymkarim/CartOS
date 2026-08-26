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
        description="Big 12oz mug for those mornings when you need three refills before the code compiles. Dishwasher safe.",
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
        description="Giant wool felt mat that makes your desk look like you have your life together. Comes with a leather strap to roll it up.",
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
    "ergonomic-chair": Product(
        id="ergonomic-chair",
        name="ErgoPro Chair",
        description="High-back mesh chair with adjustable lumbar support and customizable armrests. Keeps you comfortable during long coding sessions.",
        price_cents=34999,
        currency="eur",
        emoji="🪑",
        image_url="https://images.unsplash.com/photo-1592078615290-033ee584e267?w=800&h=800&fit=crop",
    ),
    "laptop-stand": Product(
        id="laptop-stand",
        name="Aluminum Laptop Stand",
        description="Raises your laptop screen to eye level so you stop hunching over like a goblin. Solid aluminum, folds flat.",
        price_cents=3999,
        currency="eur",
        emoji="💻",
        image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&h=800&fit=crop",
    ),
    "wireless-mouse": Product(
        id="wireless-mouse",
        name="Precision Wireless Mouse",
        description="Silent clicks so you don't annoy everyone in the office. 4000 DPI sensor, lasts weeks on a single charge.",
        price_cents=4999,
        currency="eur",
        emoji="🖱️",
        image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&h=800&fit=crop",
    ),
    "monitor-light": Product(
        id="monitor-light",
        name="Monitor Light Bar",
        description="Clips on your monitor and lights up your desk without screen glare. Your eyes will thank you at 2am.",
        price_cents=4499,
        currency="eur",
        emoji="💡",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=800&h=800&fit=crop",
    ),
}


def list_products() -> list[Product]:
    return list(PRODUCTS.values())


def get_product(product_id: str) -> Product | None:
    return PRODUCTS.get(product_id)

# DevDesk Additional Features — Design Spec

## Overview

Add 4 new features to the DevDesk payment app: Product Reviews, Wishlist, Order Tracking, and Discount Codes. Each feature is independent and can be implemented separately.

## Feature 1: Product Reviews

### Backend

**Review Model:**
```python
class Review(Base):
    __tablename__ = "reviews"
    id: int (PK)
    user_id: int (FK → users.id)
    product_id: str
    rating: int (1-5)
    title: str (max 100 chars)
    comment: str (max 1000 chars)
    created_at: datetime
    # Unique constraint on (user_id, product_id)
```

**Endpoints:**
| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/reviews/{product_id}` | GET | No | Get all reviews for a product |
| `/api/reviews` | POST | Yes | Create a review |
| `/api/reviews/{id}` | DELETE | Yes | Delete own review |

**Schemas:**
- `ReviewCreate`: `product_id`, `rating` (1-5), `title`, `comment`
- `ReviewOut`: all fields + `user_email`

**Product schema update:**
- Add `avg_rating: float` (computed from reviews)
- Add `review_count: int` (computed from reviews)

### Frontend

**Components:**
- `StarRating` — clickable star display (1-5)
- `StarRatingDisplay` — read-only star display with half-star support
- `ReviewForm` — form with star selector, title, comment
- `ReviewCard` — single review display

**Product Detail Page:**
- Average rating + review count below product name
- Review form (only if logged in)
- Review list sorted by newest first

**Product Cards:**
- Show average rating as stars below product name

---

## Feature 2: Wishlist

### Backend

**WishlistItem Model:**
```python
class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    id: int (PK)
    user_id: int (FK → users.id)
    product_id: str
    created_at: datetime
    # Unique constraint on (user_id, product_id)
```

**Endpoints:**
| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/wishlist` | GET | Yes | Get user's wishlist |
| `/api/wishlist/{product_id}` | POST | Yes | Add to wishlist |
| `/api/wishlist/{product_id}` | DELETE | Yes | Remove from wishlist |

**Schemas:**
- `WishlistItemOut`: `id`, `product_id`, `created_at`

### Frontend

**Components:**
- `WishlistButton` — heart icon toggle (filled/outline)

**Pages:**
- `/wishlist` — grid of saved products (same layout as catalog)

**Navbar:**
- Heart icon with count badge (like cart icon)

**Product Cards:**
- Heart icon in top-right corner

**Product Detail:**
- Heart icon next to "Add to Cart" button

---

## Feature 3: Order Tracking

### Backend

**Order Model Update:**
```python
# Add to existing Order model:
status: str = "pending"  # pending, processing, shipped, delivered
status_updated_at: datetime
```

**Endpoints:**
| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/orders/{id}/status` | PATCH | Yes | Update order status |

**Status values:** `pending`, `processing`, `shipped`, `delivered`

### Frontend

**Components:**
- `OrderTimeline` — 4-step vertical timeline

**Order Detail Page:**
- Timeline showing all 4 steps
- Current step highlighted (colored dot + bold text)
- Completed steps show timestamp
- Future steps grayed out

**Order Cards (Account page):**
- Status badge with color coding:
  - pending = amber
  - processing = blue
  - shipped = indigo
  - delivered = emerald

---

## Feature 4: Discount Codes

### Backend

**Coupon Model:**
```python
class Coupon(Base):
    __tablename__ = "coupons"
    id: int (PK)
    code: str (unique, uppercase)
    discount_type: str  # "percentage" or "fixed"
    discount_value: int  # percentage (1-100) or cents
    min_order_amount: int | None  # minimum order in cents
    max_uses: int | None  # null = unlimited
    uses_count: int = 0
    expires_at: datetime | None
    is_active: bool = True
    created_at: datetime
```

**Endpoints:**
| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/coupons/validate` | POST | Yes | Validate a coupon code |
| `/api/checkout/cart` | POST | Yes | Updated to accept optional `coupon_code` |

**Schemas:**
- `CouponValidate`: `code`, `order_amount`
- `CouponValidationResponse`: `valid`, `discount_amount`, `message`
- `CartCheckoutRequest` update: add optional `coupon_code: str | None`

**Validation rules:**
- Code exists and is active
- Not expired
- Not exceeded max uses
- Order meets minimum amount

### Frontend

**Cart Page:**
- Coupon input field below order summary
- "Apply" button
- Validation error messages
- Discount line in summary when applied
- "Remove" button to clear coupon

**Order Summary update:**
- Show subtotal, discount, shipping, total

---

## Implementation Order

1. **Product Reviews** — independent, adds most portfolio value
2. **Wishlist** — independent, simple UI
3. **Order Tracking** — requires order model update
4. **Discount Codes** — most complex, touches checkout flow

## Success Criteria

- [ ] Users can leave star ratings + text reviews on products
- [ ] Product cards and detail pages show average rating
- [ ] Users can save/unsave products to wishlist via heart icon
- [ ] Wishlist page shows saved products
- [ ] Order detail shows 4-step tracking timeline
- [ ] Order cards show status badge
- [ ] Users can apply coupon codes in cart
- [ ] Discount shows in order summary
- [ ] All features work for both logged-in and guest users (where applicable)

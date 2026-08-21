# DevDesk Payment App — Design Spec

## Overview

Transform the existing PayForge payment app into a polished, portfolio-worthy e-commerce store called **DevDesk** — a developer workspace gear shop. The frontend gets a complete overhaul with Tailwind CSS, React Router, and modern UI patterns. The backend receives cart functionality, password reset, bug fixes, and an expanded product catalog.

## Tech Stack

**Frontend:**
- React 19 + TypeScript + Vite (existing)
- Tailwind CSS v4 (new)
- React Router v7 (new)
- No component library — build from scratch with Tailwind

**Backend:**
- FastAPI + SQLAlchemy + PostgreSQL (existing)
- Stripe test mode (existing)
- No new dependencies beyond what's already installed

## Products

**Theme: "DevDesk" — Premium Developer Workspace Gear**

8 products, all developer/workspace focused:

| ID | Name | Price (EUR) | Description |
|---|---|---|---|
| `desk-lamp` | Focus Desk Lamp | €29.99 | Adjustable LED lamp for focused coding sessions |
| `mechanical-keyboard` | MX Artisan Keyboard | €79.99 | Hot-swappable mechanical with PBT keycaps |
| `developer-mug` | Debug Fuel Mug | €14.99 | 12oz ceramic mug, dishwasher safe |
| `ultrawide-monitor` | UltraWide 34" | €449.99 | 3440x1440 curved display, USB-C |
| `webcam-pro` | StreamCam Pro | €89.99 | 4K webcam with auto-light correction |
| `desk-mat` | Felt Desk Mat | €34.99 | Wool felt, 900x400mm, with leather strap |
| `noise-cancelling` | QuietPro Headset | €199.99 | ANC over-ear, 40hr battery |
| `usb-c-hub` | Thunderbolt Hub | €69.99 | 7-in-1 USB-C, dual HDMI, 100W PD |

Each product includes an `image_url` field pointing to a placeholder image.

## Visual Design

### Color Palette

| Role | Color | Hex |
|---|---|---|
| Background | Warm cream | `#fffbf5` |
| Surface | White | `#ffffff` |
| Primary | Coral | `#f97316` |
| Primary gradient | Coral → Rose | `#f97316` → `#f43f5e` |
| Secondary accent | Teal | `#14b8a6` |
| Success | Emerald | `#10b981` |
| Error | Red | `#ef4444` |
| Warning/Notification | Amber | `#f59e0b` |
| Text primary | Warm dark | `#1c1917` |
| Text muted | Warm gray | `#78716c` |

### Typography

- **Font:** Inter (Google Fonts) — headings and body
- **Monospace accent:** JetBrains Mono for prices/code elements
- **Scale:** Tailwind default (text-sm through text-4xl)

### Layout & Personality

- **Navbar:** Sticky top, white with warm shadow. Logo "DevDesk" left (with a small wrench emoji), nav links center, cart icon + auth right
- **Hero:** Warm gradient background (coral → rose), large friendly headline with a wave emoji, subtext, CTA button with arrow
- **Product cards:** White, rounded-2xl, coral/teal/amber top-strip (varies per product), product image, playful hover: slight tilt + colored shadow
- **Buttons:** Rounded-full, coral gradient primary with hover glow, teal secondary buttons
- **Background:** Warm cream with subtle grain texture (CSS noise pattern)
- **Footer:** Warm dark (`#1c1917`), friendly copy like "Made with ☕ and code"
- **Cart icon:** Animated count badge (bounce on add), coral colored
- **Status badges:** Pill-shaped, color-coded (paid=emerald, pending=amber, failed=red)
- **Empty states:** Friendly illustrations or emoji + encouraging copy ("Your cart is lonely 🛒")
- **Micro-interactions:** Button press effects, card hover tilts, smooth page transitions
- **Typography:** Slightly rounder, friendlier feel — use `font-feature-settings: "ss01"` for alternates

### Responsive

- **Desktop:** 4-column product grid
- **Tablet:** 2-column grid
- **Mobile:** 1-column, hamburger nav

## Pages & Routing

| Route | Page | Auth | Description |
|---|---|---|---|
| `/` | Landing | No | Hero + featured products (top 3) + trust badges + CTA |
| `/products` | Product Catalog | No | Full 8-product grid, search bar |
| `/products/:id` | Product Detail | No | Large image, full description, quantity selector, add to cart |
| `/cart` | Shopping Cart | No | Cart items list, quantity adjust, subtotal, "Proceed to Checkout" |
| `/checkout/success` | Order Success | No | Success animation, order summary, "Continue Shopping" CTA |
| `/checkout/cancel` | Checkout Cancelled | No | Friendly message, "Back to Cart" button |
| `/login` | Sign In | No | Email/password, "Forgot password?" link, "Create account" link |
| `/register` | Create Account | No | Email/password/confirm, password strength meter |
| `/forgot-password` | Forgot Password | No | Email input, submit sends reset token |
| `/reset-password` | Reset Password | No | Token (from URL params) + new password + confirm |
| `/account` | Profile & Orders | Yes | User info card, order history table with status badges |
| `/account/orders/:id` | Order Detail | Yes | Single order with timeline/status |

### Navigation

```
[DevDesk Logo]  [Products]  [Cart (3)]  [Avatar ▼]
                                              ├── My Account
                                              └── Logout

(When not logged in: [Sign In] instead of avatar)
```

### Route Protection

- `<ProtectedRoute>` wrapper checks auth context
- Redirects to `/login?redirect=/account` if not authenticated
- After login, redirects to the `redirect` param

## Auth Flow

### Login
1. User enters email + password
2. Frontend POSTs to `/api/auth/login` (OAuth2 form data)
3. Backend validates, returns JWT
4. Frontend stores JWT in localStorage, updates auth context
5. Redirect to `/account` or `redirect` param

### Register
1. User enters email + password + confirm password
2. Password strength meter shows weak/medium/strong (color bar)
3. Validation: min 8 chars, 1 uppercase, 1 lowercase, 1 number
4. Frontend POSTs to `/api/auth/register`
5. Backend creates user, returns user object
6. Auto-login after registration

### Forgot/Reset Password
1. User enters email on `/forgot-password`
2. Frontend POSTs to `/api/auth/forgot-password`
3. Backend generates reset token (expires in 1 hour), returns it (in production this would be emailed)
4. Frontend redirects to `/reset-password?token=<token>`
5. User enters new password + confirm
6. Frontend POSTs to `/api/auth/reset-password` with token + password
7. Backend validates token, updates password
8. Redirect to `/login` with success message

### Session Management
- Auth context: `{ user, token, isAuthenticated, login(), logout(), register() }`
- Token attached to API calls via Authorization header
- `/api/auth/me` called on app mount to restore session
- Logout clears localStorage + context

## Cart System

### Frontend Cart
- Cart context: `{ items, addItem(), removeItem(), updateQuantity(), clearCart(), total, itemCount }`
- Cart persisted to localStorage for guests
- Cart synced to DB for logged-in users

### Backend Cart API

| Endpoint | Method | Description |
|---|---|---|
| `/api/cart` | GET | Get current user's cart items |
| `/api/cart` | POST | Add item `{ product_id, quantity }` |
| `/api/cart/{product_id}` | PUT | Update quantity `{ quantity }` |
| `/api/cart/{product_id}` | DELETE | Remove item from cart |

### Cart Model

```python
class CartItem(Base):
    __tablename__ = "cart_items"
    id: int (PK)
    user_id: int (FK → users.id)
    product_id: str
    quantity: int
    created_at: datetime
    updated_at: datetime
```

### Checkout Flow
1. User clicks "Proceed to Checkout" in cart
2. Frontend POSTs to `/api/checkout/session` with `{ items: [{ product_id, quantity }, ...] }`
3. Backend validates all products exist, creates Stripe session with multiple line items
4. User redirected to Stripe checkout
5. On success, webhook creates order with all items, clears user's cart
6. Redirect to `/checkout/success`

**Note:** The existing `/api/checkout/session` endpoint accepts `{ product_id, quantity }` for single-product checkout. Add a new `/api/checkout/cart` endpoint that accepts `{ items: [...] }` for cart-based checkout. Both remain available.

## Backend Changes

### New Endpoints

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/auth/forgot-password` | POST | No | Generate reset token |
| `/api/auth/reset-password` | POST | No | Reset password with token |
| `/api/cart` | GET | Yes | Get user's cart |
| `/api/cart` | POST | Yes | Add to cart |
| `/api/cart/{product_id}` | PUT | Yes | Update cart item |
| `/api/cart/{product_id}` | DELETE | Yes | Remove cart item |
| `/api/orders/{id}` | GET | Yes | Single order (user-scoped) |

### New Models

```python
class CartItem(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

class PasswordReset(Base):
    __tablename__ = "password_resets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expires_at: Mapped[datetime]
    used: Mapped[bool] = mapped_column(Boolean, default=False)
```

### Bug Fixes

1. **Orders endpoint** (`routers/orders.py`): Currently returns ALL orders. Filter by `current_user.id`.
2. **Webhook indentation** (`routers/webhook.py:61-68`): The `if existing_order` check is outside the `if event.type` block — fix indentation.
3. **Password validation**: Add min 8 chars, 1 uppercase, 1 lowercase, 1 number to registration.

### Product Catalog Expansion

Update `product.py` with 8 products, add `image_url` field to Product schema.

## File Structure (Frontend)

```
src/
├── main.tsx                    # App entry with Router + providers
├── App.tsx                     # Route definitions
├── index.css                   # Tailwind directives + custom styles
├── contexts/
│   ├── AuthContext.tsx          # Auth state management
│   └── CartContext.tsx          # Cart state management
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx          # Sticky nav with logo, links, cart, auth
│   │   ├── Footer.tsx          # Dark footer with credits
│   │   └── ProtectedRoute.tsx  # Auth guard wrapper
│   ├── ui/
│   │   ├── Button.tsx          # Reusable button (primary, secondary, ghost)
│   │   ├── Badge.tsx           # Status badges
│   │   ├── Input.tsx           # Form input with label + error
│   │   ├── Spinner.tsx         # Loading spinner
│   │   └── PasswordStrength.tsx # Password strength meter
│   ├── ProductCard.tsx         # Product card for grid display
│   ├── CartItem.tsx            # Single cart item row
│   └── OrderCard.tsx           # Order summary card
├── pages/
│   ├── Landing.tsx             # Hero + featured + trust badges
│   ├── ProductCatalog.tsx      # Full product grid
│   ├── ProductDetail.tsx       # Single product view
│   ├── Cart.tsx                # Shopping cart
│   ├── CheckoutSuccess.tsx     # Post-payment success
│   ├── CheckoutCancel.tsx      # Payment cancelled
│   ├── Login.tsx               # Sign in form
│   ├── Register.tsx            # Create account form
│   ├── ForgotPassword.tsx      # Forgot password form
│   ├── ResetPassword.tsx       # Reset password form
│   ├── Account.tsx             # Profile + order history
│   └── OrderDetail.tsx         # Single order view
├── services/
│   └── api.ts                  # API client with auth headers
└── types/
    └── index.ts                # TypeScript types
```

## Implementation Order

1. **Frontend foundation** — Install Tailwind + React Router, set up layout (Navbar, Footer), route structure
2. **Auth UI** — Login, Register, ForgotPassword, ResetPassword pages + AuthContext
3. **Product pages** — Landing, Catalog, Detail with new product data and placeholder images
4. **Cart system** — CartContext, Cart page, checkout flow integration
5. **Account pages** — Account profile, OrderDetail with protected routes
6. **Backend additions** — Cart API, password reset, bug fixes
7. **Polish** — Animations, responsive tweaks, error states, loading states

## Success Criteria

- [ ] All 10 pages render correctly with proper routing
- [ ] Auth flow works: register → login → access protected routes → logout
- [ ] Cart works: add items → adjust quantities → checkout via Stripe → order saved
- [ ] Password reset flow works end-to-end
- [ ] Orders are user-scoped (not visible to other users)
- [ ] Responsive on mobile, tablet, desktop
- [ ] Visual design matches spec: gradient hero, colored cards, animations
- [ ] No TypeScript errors, no console errors
- [ ] Stripe checkout completes successfully in test mode

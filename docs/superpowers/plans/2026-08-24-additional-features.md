# DevDesk Additional Features Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Product Reviews, Wishlist, Order Tracking, and Discount Codes to the DevDesk payment app.

**Architecture:** Each feature is independent with its own backend model, API endpoints, and frontend components. Features are implemented in order of complexity: Reviews → Wishlist → Order Tracking → Discount Codes.

**Tech Stack:** React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7, FastAPI, SQLAlchemy, Stripe, PostgreSQL

## Global Constraints

- All frontend styling uses Tailwind CSS v4 utility classes
- All pages use React Router v7 for navigation
- Auth tokens stored in localStorage, attached via Authorization header
- Backend uses SQLAlchemy models with PostgreSQL
- Stripe integration uses test mode (`sk_test_` prefix required)
- Color palette: coral primary (`#f97316`), teal secondary (`#14b8a6`), warm background (`#fffbf5`)
- Font: Inter from Google Fonts
- All API calls go through a centralized `api.ts` service with auth headers

---

## Branch Strategy

| Branch | Tasks | Description |
|---|---|---|
| `feature/product-reviews` | Task 1, 2 | Review model, API, and UI components |
| `feature/wishlist` | Task 3, 4 | Wishlist model, API, and UI components |
| `feature/order-tracking` | Task 5, 6 | Order status field, timeline UI |
| `feature/discount-codes` | Task 7, 8 | Coupon model, validation, checkout integration |

---

## Task 1: Product Reviews — Backend

**Branch:** `feature/product-reviews`

**Files:**
- Create: `backend/app/models.py` (add Review model)
- Create: `backend/app/schemas.py` (add Review schemas)
- Create: `backend/app/routers/reviews.py`
- Modify: `backend/app/main.py` (register router)

**Interfaces:**
- Produces: `Review` model, `POST /api/reviews`, `GET /api/reviews/{product_id}`, `DELETE /api/reviews/{id}`
- Consumes: `User` model, `Product` schema

- [ ] **Step 1: Add Review model**

```python
# Add to backend/app/models.py

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    comment: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship()

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product_review"),
    )
```

- [ ] **Step 2: Add Review schemas**

```python
# Add to backend/app/schemas.py

class ReviewCreate(BaseModel):
    product_id: str
    rating: int = Field(ge=1, le=5)
    title: str = Field(max_length=100)
    comment: str = Field(max_length=1000)

class ReviewOut(BaseModel):
    id: int
    user_id: int
    product_id: str
    rating: int
    title: str
    comment: str
    created_at: datetime
    user_email: str

    model_config = ConfigDict(from_attributes=True)
```

- [ ] **Step 3: Create reviews router**

```python
# backend/app/routers/reviews.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Review, User
from app.schemas import ReviewCreate, ReviewOut

router = APIRouter(
    prefix="/api/reviews",
    tags=["Reviews"],
)


@router.get("/{product_id}", response_model=list[ReviewOut])
def get_reviews(
    product_id: str,
    db: Session = Depends(get_db),
):
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    result = []
    for review in reviews:
        user = db.get(User, review.user_id)
        result.append(ReviewOut(
            id=review.id,
            user_id=review.user_id,
            product_id=review.product_id,
            rating=review.rating,
            title=review.title,
            comment=review.comment,
            created_at=review.created_at,
            user_email=user.email if user else "Unknown",
        ))

    return result


@router.post(
    "",
    response_model=ReviewOut,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Review)
        .filter(
            Review.user_id == current_user.id,
            Review.product_id == review_data.product_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already reviewed this product.",
        )

    review = Review(
        user_id=current_user.id,
        product_id=review_data.product_id,
        rating=review_data.rating,
        title=review_data.title,
        comment=review_data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    return ReviewOut(
        id=review.id,
        user_id=review.user_id,
        product_id=review.product_id,
        rating=review.rating,
        title=review.title,
        comment=review.comment,
        created_at=review.created_at,
        user_email=current_user.email,
    )


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    review = db.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews.",
        )

    db.delete(review)
    db.commit()
```

- [ ] **Step 4: Register reviews router**

```python
# backend/app/main.py — add import and include

from app.routers import auth, cart, checkout, orders, products, reviews, webhook

app.include_router(reviews.router)
```

- [ ] **Step 5: Test reviews API**

```bash
# Create a review
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"product_id": "desk-lamp", "rating": 5, "title": "Great lamp!", "comment": "Perfect for my desk."}'

# Get reviews for a product
curl http://localhost:8000/api/reviews/desk-lamp
```

- [ ] **Step 6: Commit**

```bash
git add backend/
git commit -m "add product reviews backend - model, schemas, and API endpoints"
```

---

## Task 2: Product Reviews — Frontend

**Branch:** `feature/product-reviews` (continued)

**Files:**
- Create: `frontend/src/components/StarRating.tsx`
- Create: `frontend/src/components/ReviewForm.tsx`
- Create: `frontend/src/components/ReviewCard.tsx`
- Modify: `frontend/src/pages/ProductDetail.tsx`
- Modify: `frontend/src/components/ProductCard.tsx`

**Interfaces:**
- Consumes: `POST /api/reviews`, `GET /api/reviews/{product_id}`, `DELETE /api/reviews/{id}`
- Produces: Star rating display, review form, review list

- [ ] **Step 1: Create StarRating component**

```typescript
// frontend/src/components/StarRating.tsx

import { useState } from "react";

interface StarRatingProps {
  rating: number;
  onRate?: (rating: number) => void;
  readonly?: boolean;
  size?: "sm" | "md" | "lg";
}

export default function StarRating({
  rating,
  onRate,
  readonly = false,
  size = "md",
}: StarRatingProps) {
  const [hovered, setHovered] = useState(0);

  const sizes = {
    sm: "h-4 w-4",
    md: "h-5 w-5",
    lg: "h-6 w-6",
  };

  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          type="button"
          disabled={readonly}
          onClick={() => onRate?.(star)}
          onMouseEnter={() => !readonly && setHovered(star)}
          onMouseLeave={() => !readonly && setHovered(0)}
          className={`${readonly ? "cursor-default" : "cursor-pointer"} transition-colors`}
        >
          <svg
            className={`${sizes[size]} ${
              star <= (hovered || rating)
                ? "text-warning fill-warning"
                : "text-black/20 fill-black/20"
            }`}
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        </button>
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Create ReviewForm component**

```typescript
// frontend/src/components/ReviewForm.tsx

import { useState, type FormEvent } from "react";
import { api } from "../services/api";
import StarRating from "./StarRating";
import Button from "./ui/Button";
import Input from "./ui/Input";

interface ReviewFormProps {
  productId: string;
  onReviewAdded: () => void;
}

export default function ReviewForm({ productId, onReviewAdded }: ReviewFormProps) {
  const [rating, setRating] = useState(0);
  const [title, setTitle] = useState("");
  const [comment, setComment] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    if (rating === 0) {
      setError("Please select a rating");
      return;
    }

    setIsLoading(true);

    try {
      await api.post("/api/reviews", {
        product_id: productId,
        rating,
        title,
        comment,
      });
      setRating(0);
      setTitle("");
      setComment("");
      onReviewAdded();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit review");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-surface rounded-xl p-6 shadow-sm space-y-4">
      <h3 className="text-lg font-semibold">Write a Review</h3>

      {error && (
        <div className="bg-error/10 text-error text-sm p-3 rounded-lg">
          {error}
        </div>
      )}

      <div>
        <label className="block text-sm font-medium mb-2">Rating</label>
        <StarRating rating={rating} onRate={setRating} size="lg" />
      </div>

      <Input
        label="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Summarize your experience"
        required
      />

      <div className="space-y-1">
        <label className="block text-sm font-medium">Comment</label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Tell others what you think about this product"
          rows={4}
          className="w-full rounded-lg border border-black/10 bg-surface px-4 py-2.5 text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
          required
        />
      </div>

      <Button type="submit" isLoading={isLoading}>
        Submit Review
      </Button>
    </form>
  );
}
```

- [ ] **Step 3: Create ReviewCard component**

```typescript
// frontend/src/components/ReviewCard.tsx

import type { Review } from "../types";
import StarRating from "./StarRating";

interface ReviewCardProps {
  review: Review;
  onDelete?: (id: number) => void;
  isOwnReview?: boolean;
}

export default function ReviewCard({ review, onDelete, isOwnReview }: ReviewCardProps) {
  const date = new Date(review.created_at).toLocaleDateString("en-IE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <div className="border-b border-black/5 py-4 last:border-0">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-primary/10 text-primary flex items-center justify-center text-sm font-medium">
            {review.user_email.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="text-sm font-medium">{review.user_email}</p>
            <p className="text-xs text-text-muted">{date}</p>
          </div>
        </div>
        {isOwnReview && onDelete && (
          <button
            onClick={() => onDelete(review.id)}
            className="text-xs text-error hover:text-error/80"
          >
            Delete
          </button>
        )}
      </div>
      <StarRating rating={review.rating} readonly size="sm" />
      <p className="font-medium mt-1">{review.title}</p>
      <p className="text-sm text-text-muted mt-1">{review.comment}</p>
    </div>
  );
}
```

- [ ] **Step 4: Add Review type**

```typescript
// Add to frontend/src/types/index.ts

export interface Review {
  id: number;
  user_id: number;
  product_id: string;
  rating: number;
  title: string;
  comment: string;
  created_at: string;
  user_email: string;
}
```

- [ ] **Step 5: Update ProductDetail page with reviews**

Update `ProductDetail.tsx` to fetch and display reviews, and show the review form:

```typescript
// Add imports
import StarRating from "../components/StarRating";
import ReviewForm from "../components/ReviewForm";
import ReviewCard from "../components/ReviewCard";
import { useAuth } from "../contexts/AuthContext";
import type { Review } from "../types";

// Add state
const [reviews, setReviews] = useState<Review[]>([]);
const { isAuthenticated } = useAuth();

// Add fetch function
async function fetchReviews() {
  try {
    const data = await api.get<Review[]>(`/api/reviews/${id}`);
    setReviews(data);
  } catch (err) {
    console.error("Failed to fetch reviews:", err);
  }
}

useEffect(() => {
  if (id) fetchReviews();
}, [id]);

// Add to JSX (after product details, before closing div)
<section className="mt-12">
  <h2 className="text-2xl font-bold mb-4">
    Reviews ({reviews.length})
    {reviews.length > 0 && (
      <span className="ml-2 text-lg font-normal text-text-muted">
        · {avgRating.toFixed(1)} stars
      </span>
    )}
  </h2>

  {isAuthenticated && (
    <div className="mb-6">
      <ReviewForm productId={product.id} onReviewAdded={fetchReviews} />
    </div>
  )}

  <div className="space-y-2">
    {reviews.map((review) => (
      <ReviewCard key={review.id} review={review} />
    ))}
  </div>
</section>
```

- [ ] **Step 6: Update ProductCard with rating**

Add average rating display to `ProductCard.tsx`:

```typescript
// Add to ProductCard component
const avgRating = reviews.length > 0
  ? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length
  : 0;

// Add below product name in JSX
{avgRating > 0 && (
  <div className="flex items-center gap-1 mt-1">
    <StarRating rating={Math.round(avgRating)} readonly size="sm" />
    <span className="text-xs text-text-muted">({reviews.length})</span>
  </div>
)}
```

- [ ] **Step 7: Verify frontend compiles**

```bash
cd frontend && npm run build
```

- [ ] **Step 8: Commit and merge**

```bash
git add frontend/
git commit -m "add product reviews frontend - star ratings, review form, and display"

# Merge to main
git checkout main
git merge feature/product-reviews
```

---

## Task 3: Wishlist — Backend

**Branch:** `feature/wishlist`

**Files:**
- Create: `backend/app/models.py` (add WishlistItem model)
- Create: `backend/app/schemas.py` (add Wishlist schemas)
- Create: `backend/app/routers/wishlist.py`
- Modify: `backend/app/main.py` (register router)

**Interfaces:**
- Produces: `WishlistItem` model, `POST/DELETE /api/wishlist/{product_id}`, `GET /api/wishlist`
- Consumes: `User` model

- [ ] **Step 1: Add WishlistItem model**

```python
# Add to backend/app/models.py

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship()

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product_wishlist"),
    )
```

- [ ] **Step 2: Add Wishlist schemas**

```python
# Add to backend/app/schemas.py

class WishlistItemOut(BaseModel):
    id: int
    product_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

- [ ] **Step 3: Create wishlist router**

```python
# backend/app/routers/wishlist.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, WishlistItem
from app.schemas import WishlistItemOut
from app.product import get_product

router = APIRouter(
    prefix="/api/wishlist",
    tags=["Wishlist"],
)


@router.get("", response_model=list[WishlistItemOut])
def get_wishlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(WishlistItem)
        .filter(WishlistItem.user_id == current_user.id)
        .order_by(WishlistItem.created_at.desc())
        .all()
    )


@router.post(
    "/{product_id}",
    response_model=WishlistItemOut,
    status_code=status.HTTP_201_CREATED,
)
def add_to_wishlist(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    existing = (
        db.query(WishlistItem)
        .filter(
            WishlistItem.user_id == current_user.id,
            WishlistItem.product_id == product_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product already in wishlist.",
        )

    item = WishlistItem(
        user_id=current_user.id,
        product_id=product_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_wishlist(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(WishlistItem)
        .filter(
            WishlistItem.user_id == current_user.id,
            WishlistItem.product_id == product_id,
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in wishlist.",
        )

    db.delete(item)
    db.commit()
```

- [ ] **Step 4: Register wishlist router**

```python
# backend/app/main.py — add import and include

from app.routers import auth, cart, checkout, orders, products, reviews, webhook, wishlist

app.include_router(wishlist.router)
```

- [ ] **Step 5: Commit**

```bash
git add backend/
git commit -m "add wishlist backend - model, schemas, and API endpoints"
```

---

## Task 4: Wishlist — Frontend

**Branch:** `feature/wishlist` (continued)

**Files:**
- Create: `frontend/src/components/WishlistButton.tsx`
- Create: `frontend/src/pages/Wishlist.tsx`
- Modify: `frontend/src/components/layout/Navbar.tsx`
- Modify: `frontend/src/components/ProductCard.tsx`
- Modify: `frontend/src/pages/ProductDetail.tsx`
- Modify: `frontend/src/App.tsx` (add route)

**Interfaces:**
- Consumes: `POST/DELETE /api/wishlist/{product_id}`, `GET /api/wishlist`
- Produces: Heart icon toggle, wishlist page

- [ ] **Step 1: Create WishlistButton component**

```typescript
// frontend/src/components/WishlistButton.tsx

import { useState, useEffect } from "react";
import { api } from "../services/api";
import { useAuth } from "../contexts/AuthContext";

interface WishlistButtonProps {
  productId: string;
  size?: "sm" | "md" | "lg";
}

export default function WishlistButton({ productId, size = "md" }: WishlistButtonProps) {
  const [isInWishlist, setIsInWishlist] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { isAuthenticated } = useAuth();

  const sizes = {
    sm: "h-4 w-4",
    md: "h-5 w-5",
    lg: "h-6 w-6",
  };

  useEffect(() => {
    if (!isAuthenticated) return;

    api
      .get<{ product_id: string }[]>("/api/wishlist")
      .then((items) => setIsInWishlist(items.some((i) => i.product_id === productId)))
      .catch(console.error);
  }, [productId, isAuthenticated]);

  async function toggleWishlist() {
    if (!isAuthenticated) return;

    setIsLoading(true);
    try {
      if (isInWishlist) {
        await api.delete(`/api/wishlist/${productId}`);
        setIsInWishlist(false);
      } else {
        await api.post(`/api/wishlist/${productId}`);
        setIsInWishlist(true);
      }
    } catch (err) {
      console.error("Failed to toggle wishlist:", err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <button
      onClick={toggleWishlist}
      disabled={isLoading || !isAuthenticated}
      className={`p-1 rounded-full transition-colors ${
        isInWishlist
          ? "text-error hover:text-error/80"
          : "text-text-muted hover:text-error"
      }`}
      title={isInWishlist ? "Remove from wishlist" : "Add to wishlist"}
    >
      <svg
        className={sizes[size]}
        fill={isInWishlist ? "currentColor" : "none"}
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
        />
      </svg>
    </button>
  );
}
```

- [ ] **Step 2: Create Wishlist page**

```typescript
// frontend/src/pages/Wishlist.tsx

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import type { Product } from "../types";
import ProductCard from "../components/ProductCard";
import Spinner from "../components/ui/Spinner";
import Button from "../components/ui/Button";

export default function Wishlist() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchWishlist() {
      try {
        const wishlistItems = await api.get<{ product_id: string }[]>("/api/wishlist");
        const allProducts = await api.get<Product[]>("/api/products");
        const wishlistProducts = allProducts.filter((p) =>
          wishlistItems.some((i) => i.product_id === p.id)
        );
        setProducts(wishlistProducts);
      } catch (err) {
        console.error("Failed to fetch wishlist:", err);
      } finally {
        setIsLoading(false);
      }
    }

    fetchWishlist();
  }, []);

  if (isLoading) return <Spinner />;

  if (products.length === 0) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <div className="text-5xl mb-4">❤️</div>
        <h1 className="text-2xl font-bold mb-2">Your wishlist is empty</h1>
        <p className="text-text-muted mb-6">
          Save products you love by clicking the heart icon.
        </p>
        <Link to="/products">
          <Button>Browse Products</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold mb-8">My Wishlist</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Add wishlist route to App.tsx**

```typescript
// Add import
import Wishlist from "./pages/Wishlist";

// Add route
<Route path="/wishlist" element={<Wishlist />} />
```

- [ ] **Step 4: Update Navbar with wishlist icon**

Add heart icon to Navbar (next to cart icon):

```typescript
import WishlistButton from "../WishlistButton";

// Add to Navbar JSX (next to cart link)
<Link
  to="/wishlist"
  className="relative p-2 text-text-muted hover:text-text transition-colors"
>
  <svg
    className="h-6 w-6"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
    strokeWidth={2}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
    />
  </svg>
</Link>
```

- [ ] **Step 5: Add WishlistButton to ProductCard**

Add heart icon to product cards:

```typescript
import WishlistButton from "./WishlistButton";

// Add to ProductCard JSX (inside the Link, top-right corner)
<div className="absolute top-2 right-2 z-10">
  <WishlistButton productId={product.id} size="sm" />
</div>

// Add relative positioning to the Link
className="group relative bg-surface rounded-xl overflow-hidden..."
```

- [ ] **Step 6: Add WishlistButton to ProductDetail**

Add heart icon next to Add to Cart button:

```typescript
import WishlistButton from "../components/WishlistButton";

// Add to ProductDetail JSX (next to Add to Cart button)
<div className="flex gap-2">
  <Button size="lg" className="flex-1" isLoading={isAdding} onClick={handleAddToCart}>
    Add to Cart
  </Button>
  <WishlistButton productId={product.id} size="lg" />
</div>
```

- [ ] **Step 7: Verify frontend compiles**

```bash
cd frontend && npm run build
```

- [ ] **Step 8: Commit and merge**

```bash
git add frontend/
git commit -m "add wishlist frontend - heart icon, wishlist page, and toggle functionality"

# Merge to main
git checkout main
git merge feature/wishlist
```

---

## Task 5: Order Tracking — Backend

**Branch:** `feature/order-tracking`

**Files:**
- Modify: `backend/app/models.py` (add status fields to Order)
- Modify: `backend/app/schemas.py` (add status to OrderOut)
- Modify: `backend/app/routers/orders.py` (add status update endpoint)

**Interfaces:**
- Produces: `PATCH /api/orders/{id}/status`, status field on Order
- Consumes: `Order` model

- [ ] **Step 1: Add status fields to Order model**

```python
# Add to Order model in backend/app/models.py

status: Mapped[str] = mapped_column(
    String(20),
    nullable=False,
    default="pending",
)

status_updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    default=lambda: datetime.now(timezone.utc),
)
```

- [ ] **Step 2: Update OrderOut schema**

```python
# Update OrderOut in backend/app/schemas.py

class OrderOut(BaseModel):
    id: int
    stripe_session_id: str
    product_id: str
    quantity: int
    payment_status: str
    amount_total: int | None
    customer_email: str | None
    created_at: datetime
    status: str
    status_updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

- [ ] **Step 3: Add status update endpoint**

```python
# Add to backend/app/routers/orders.py

class StatusUpdate(BaseModel):
    status: str

@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    status_update: StatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    valid_statuses = ["pending", "processing", "shipped", "delivered"]
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
        )

    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id,
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    order.status = status_update.status
    order.status_updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(order)

    return order
```

- [ ] **Step 4: Update webhook to set initial status**

```python
# Update webhook.py - add status to new_order creation

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
```

- [ ] **Step 5: Commit**

```bash
git add backend/
git commit -m "add order tracking backend - status field and update endpoint"
```

---

## Task 6: Order Tracking — Frontend

**Branch:** `feature/order-tracking` (continued)

**Files:**
- Create: `frontend/src/components/OrderTimeline.tsx`
- Modify: `frontend/src/pages/OrderDetail.tsx`
- Modify: `frontend/src/components/OrderCard.tsx`
- Modify: `frontend/src/types/index.ts`

**Interfaces:**
- Consumes: `PATCH /api/orders/{id}/status`, `status` field on Order
- Produces: Timeline component, status badges

- [ ] **Step 1: Update Order type**

```typescript
// Update Order type in frontend/src/types/index.ts

export interface Order {
  id: number;
  stripe_session_id: string;
  product_id: string;
  quantity: number;
  payment_status: string;
  amount_total: number | null;
  customer_email: string | null;
  created_at: string;
  status: string;
  status_updated_at: string;
}
```

- [ ] **Step 2: Create OrderTimeline component**

```typescript
// frontend/src/components/OrderTimeline.tsx

interface OrderTimelineProps {
  status: string;
  createdAt: string;
  statusUpdatedAt: string;
}

const steps = [
  { key: "pending", label: "Order Placed" },
  { key: "processing", label: "Processing" },
  { key: "shipped", label: "Shipped" },
  { key: "delivered", label: "Delivered" },
];

export default function OrderTimeline({
  status,
  createdAt,
  statusUpdatedAt,
}: OrderTimelineProps) {
  const currentIndex = steps.findIndex((s) => s.key === status);

  return (
    <div className="space-y-0">
      {steps.map((step, index) => {
        const isCompleted = index <= currentIndex;
        const isCurrent = index === currentIndex;

        return (
          <div key={step.key} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div
                className={`h-8 w-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  isCompleted
                    ? "bg-primary text-white"
                    : "bg-black/10 text-text-muted"
                } ${isCurrent ? "ring-2 ring-primary/30" : ""}`}
              >
                {isCompleted ? "✓" : index + 1}
              </div>
              {index < steps.length - 1 && (
                <div
                  className={`w-0.5 h-8 ${
                    index < currentIndex ? "bg-primary" : "bg-black/10"
                  }`}
                />
              )}
            </div>
            <div className="pb-8">
              <p
                className={`font-medium ${
                  isCompleted ? "text-text" : "text-text-muted"
                }`}
              >
                {step.label}
              </p>
              {isCompleted && (
                <p className="text-xs text-text-muted">
                  {new Date(
                    index === 0 ? createdAt : statusUpdatedAt
                  ).toLocaleDateString("en-IE", {
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

- [ ] **Step 3: Update OrderDetail page with timeline**

```typescript
// Add to OrderDetail.tsx

import OrderTimeline from "../components/OrderTimeline";

// Add to JSX (inside the order card, after the details)
<div className="mt-6 pt-6 border-t border-black/5">
  <h3 className="font-semibold mb-4">Order Status</h3>
  <OrderTimeline
    status={order.status}
    createdAt={order.created_at}
    statusUpdatedAt={order.status_updated_at}
  />
</div>
```

- [ ] **Step 4: Update OrderCard with status badge**

```typescript
// Update OrderCard.tsx

const statusColors: Record<string, string> = {
  pending: "bg-warning/10 text-warning",
  processing: "bg-blue-500/10 text-blue-500",
  shipped: "bg-indigo-500/10 text-indigo-500",
  delivered: "bg-success/10 text-success",
};

// Add to JSX
<span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${statusColors[order.status] || "bg-black/5 text-text-muted"}`}>
  {order.status}
</span>
```

- [ ] **Step 5: Verify frontend compiles**

```bash
cd frontend && npm run build
```

- [ ] **Step 6: Commit and merge**

```bash
git add frontend/
git commit -m "add order tracking frontend - timeline component and status badges"

# Merge to main
git checkout main
git merge feature/order-tracking
```

---

## Task 7: Discount Codes — Backend

**Branch:** `feature/discount-codes`

**Files:**
- Create: `backend/app/models.py` (add Coupon model)
- Create: `backend/app/schemas.py` (add Coupon schemas)
- Create: `backend/app/routers/coupons.py`
- Modify: `backend/app/routers/checkout.py` (apply coupon)
- Modify: `backend/app/main.py` (register router)

**Interfaces:**
- Produces: `Coupon` model, `POST /api/coupons/validate`, coupon in checkout
- Consumes: `Order` model, Stripe checkout

- [ ] **Step 1: Add Coupon model**

```python
# Add to backend/app/models.py

class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    discount_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    discount_value: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    min_order_amount: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    max_uses: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    uses_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
```

- [ ] **Step 2: Add Coupon schemas**

```python
# Add to backend/app/schemas.py

class CouponValidate(BaseModel):
    code: str
    order_amount: int

class CouponValidationResponse(BaseModel):
    valid: bool
    discount_amount: int
    message: str
```

- [ ] **Step 3: Create coupons router**

```python
# backend/app/routers/coupons.py

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

    if coupon.expires_at and coupon.expires_at < datetime.now(timezone.utc):
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
```

- [ ] **Step 4: Register coupons router**

```python
# backend/app/main.py — add import and include

from app.routers import auth, cart, checkout, coupons, orders, products, reviews, webhook, wishlist

app.include_router(coupons.router)
```

- [ ] **Step 5: Update checkout to accept coupon**

Update `CartCheckoutRequest` and `create_cart_checkout_session` in `checkout.py`:

```python
# Update CartCheckoutRequest
class CartCheckoutRequest(BaseModel):
    items: list[CheckoutRequest]
    coupon_code: str | None = None

# Update create_cart_checkout_session to apply discount
# After calculating line_items, if coupon_code is provided:
# 1. Validate coupon
# 2. Apply discount to session
# 3. Increment coupon uses_count
```

- [ ] **Step 6: Commit**

```bash
git add backend/
git commit -m "add discount codes backend - coupon model, validation, and checkout integration"
```

---

## Task 8: Discount Codes — Frontend

**Branch:** `feature/discount-codes` (continued)

**Files:**
- Modify: `frontend/src/pages/Cart.tsx`
- Modify: `frontend/src/contexts/CartContext.tsx`

**Interfaces:**
- Consumes: `POST /api/coupons/validate`, coupon in checkout
- Produces: Coupon input in cart, discount display

- [ ] **Step 1: Add coupon state to CartContext**

```typescript
// Add to CartContext

interface CartContextType {
  // ... existing
  couponCode: string | null;
  discountAmount: number;
  applyCoupon: (code: string) => Promise<boolean>;
  removeCoupon: () => void;
}

// Add state
const [couponCode, setCouponCode] = useState<string | null>(null);
const [discountAmount, setDiscountAmount] = useState(0);

// Add functions
async function applyCoupon(code: string): Promise<boolean> {
  try {
    const data = await api.post<{ valid: boolean; discount_amount: number; message: string }>(
      "/api/coupons/validate",
      { code, order_amount: total }
    );
    if (data.valid) {
      setCouponCode(code);
      setDiscountAmount(data.discount_amount);
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

function removeCoupon() {
  setCouponCode(null);
  setDiscountAmount(0);
}
```

- [ ] **Step 2: Update Cart page with coupon input**

```typescript
// Add to Cart.tsx

const { couponCode, discountAmount, applyCoupon, removeCoupon } = useCart();
const [couponInput, setCouponInput] = useState("");
const [couponError, setCouponError] = useState("");
const [isApplyingCoupon, setIsApplyingCoupon] = useState(false);

async function handleApplyCoupon() {
  setCouponError("");
  setIsApplyingCoupon(true);
  const success = await applyCoupon(couponInput);
  if (!success) {
    setCouponError("Invalid coupon code");
  }
  setIsApplyingCoupon(false);
}

// Add to order summary JSX
<div className="mt-4 space-y-2">
  {couponCode ? (
    <div className="flex items-center justify-between text-sm">
      <span className="text-success">
        Coupon: {couponCode}
        <button onClick={removeCoupon} className="ml-2 text-error">(remove)</button>
      </span>
      <span className="text-success">-€{discountAmount / 100}</span>
    </div>
  ) : (
    <div className="flex gap-2">
      <input
        type="text"
        value={couponInput}
        onChange={(e) => setCouponInput(e.target.value)}
        placeholder="Coupon code"
        className="flex-1 rounded-lg border border-black/10 px-3 py-2 text-sm"
      />
      <Button
        variant="secondary"
        size="sm"
        onClick={handleApplyCoupon}
        isLoading={isApplyingCoupon}
      >
        Apply
      </Button>
    </div>
  )}
  {couponError && <p className="text-xs text-error">{couponError}</p>}
</div>

// Update total to show discount
<div className="border-t border-black/5 pt-2 mt-2">
  {discountAmount > 0 && (
    <div className="flex justify-between text-sm text-success mb-1">
      <span>Discount</span>
      <span>-€{discountAmount / 100}</span>
    </div>
  )}
  <div className="flex justify-between font-semibold text-base">
    <span>Total</span>
    <span>€{(total - discountAmount) / 100}</span>
  </div>
</div>
```

- [ ] **Step 3: Update checkout to send coupon code**

```typescript
// Update handleCheckout in Cart.tsx

const data = await api.post<{ checkout_url: string; session_id: string }>(
  "/api/checkout/cart",
  {
    items: items.map(({ product_id, quantity }) => ({ product_id, quantity })),
    coupon_code: couponCode,
  }
);
```

- [ ] **Step 4: Verify frontend compiles**

```bash
cd frontend && npm run build
```

- [ ] **Step 5: Commit and merge**

```bash
git add frontend/
git commit -m "add discount codes frontend - coupon input, validation, and checkout integration"

# Merge to main
git checkout main
git merge feature/discount-codes
```

---

## Task 9: Final Integration Test

- [ ] **Step 1: Start backend**

```bash
cd backend
python -m uvicorn main:app --reload
```

- [ ] **Step 2: Start frontend**

```bash
cd frontend
npm run dev
```

- [ ] **Step 3: Test all features**

1. **Reviews:** Leave a review on a product, verify it shows on product page
2. **Wishlist:** Heart a product, check wishlist page, remove from wishlist
3. **Order Tracking:** Place an order, check order detail shows timeline
4. **Discount Codes:** Apply a coupon in cart, verify discount shows

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "add reviews, wishlist, order tracking, and discount codes features"
```

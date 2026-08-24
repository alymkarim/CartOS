import { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../services/api";
import { useCart } from "../contexts/CartContext";
import { useAuth } from "../contexts/AuthContext";
import type { Product, Review } from "../types";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";
import ReviewForm from "../components/ReviewForm";
import ReviewCard from "../components/ReviewCard";

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [reviews, setReviews] = useState<Review[]>([]);
  const { addItem } = useCart();
  const { isAuthenticated } = useAuth();

  const fetchReviews = useCallback(async () => {
    if (!id) return;
    try {
      const data = await api.get<Review[]>(`/api/reviews/${id}`);
      setReviews(data);
    } catch (err) {
      console.error("Failed to fetch reviews:", err);
    }
  }, [id]);

  useEffect(() => {
    api
      .get<Product[]>("/api/products")
      .then((products) => setProduct(products.find((p) => p.id === id) ?? null))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, [id]);

  useEffect(() => {
    fetchReviews();
  }, [fetchReviews]);

  if (isLoading) return <Spinner />;

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center">
        <h1 className="text-2xl font-bold mb-4">Product not found</h1>
        <Link to="/products">
          <Button variant="secondary">Back to Products</Button>
        </Link>
      </div>
    );
  }

  const price = new Intl.NumberFormat("en-IE", {
    style: "currency",
    currency: product.currency.toUpperCase(),
  }).format(product.price_cents / 100);

  async function handleAddToCart() {
    if (!product) return;
    setIsAdding(true);
    try {
      await addItem(product.id, quantity);
    } catch (err) {
      console.error("Failed to add to cart:", err);
    } finally {
      setIsAdding(false);
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link
        to="/products"
        className="text-sm text-text-muted hover:text-text transition-colors mb-6 inline-block"
      >
        ← Back to Products
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div className="aspect-square rounded-xl overflow-hidden bg-black/5">
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover"
          />
        </div>

        <div>
          <h1 className="text-3xl font-bold">{product.name}</h1>
          <p className="text-3xl font-bold text-primary mt-2">{price}</p>
          <p className="text-text-muted mt-4 leading-relaxed">
            {product.description}
          </p>

          <div className="mt-8 space-y-4">
            <div className="flex items-center gap-4">
              <label className="text-sm font-medium">Quantity</label>
              <div className="flex items-center border border-black/10 rounded-lg">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="px-3 py-2 text-text-muted hover:text-text transition-colors"
                >
                  −
                </button>
                <span className="px-4 py-2 text-sm font-medium">{quantity}</span>
                <button
                  onClick={() => setQuantity(Math.min(10, quantity + 1))}
                  className="px-3 py-2 text-text-muted hover:text-text transition-colors"
                >
                  +
                </button>
              </div>
            </div>

            <Button
              size="lg"
              className="w-full"
              isLoading={isAdding}
              onClick={handleAddToCart}
            >
              Add to Cart
            </Button>

            <p className="text-xs text-text-muted text-center">
              Secure checkout powered by Stripe
            </p>
          </div>
        </div>
      </div>

      <section className="mt-12">
        <h2 className="text-2xl font-bold mb-4">
          Reviews ({reviews.length})
          {reviews.length > 0 && (
            <span className="ml-2 text-lg font-normal text-text-muted">
              · {(reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1)} stars
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
    </div>
  );
}

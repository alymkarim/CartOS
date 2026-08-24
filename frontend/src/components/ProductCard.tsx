import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import type { Product, Review } from "../types";
import StarRating from "./StarRating";

export default function ProductCard({ product }: { product: Product }) {
  const [reviews, setReviews] = useState<Review[]>([]);

  useEffect(() => {
    api
      .get<Review[]>(`/api/reviews/${product.id}`)
      .then(setReviews)
      .catch(console.error);
  }, [product.id]);

  const avgRating =
    reviews.length > 0
      ? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length
      : 0;

  const price = new Intl.NumberFormat("en-IE", {
    style: "currency",
    currency: product.currency.toUpperCase(),
  }).format(product.price_cents / 100);

  return (
    <Link
      to={`/products/${product.id}`}
      className="group bg-surface rounded-xl overflow-hidden shadow-sm hover:shadow-lg hover:shadow-primary/10 transition-all duration-300 hover:-translate-y-1"
    >
      <div className="aspect-square overflow-hidden bg-black/5">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-text group-hover:text-primary transition-colors">
          {product.name}
        </h3>
        {avgRating > 0 && (
          <div className="flex items-center gap-1 mt-1">
            <StarRating rating={Math.round(avgRating)} readonly size="sm" />
            <span className="text-xs text-text-muted">({reviews.length})</span>
          </div>
        )}
        <p className="text-sm text-text-muted mt-1 line-clamp-2">
          {product.description}
        </p>
        <p className="text-lg font-bold text-text mt-3">{price}</p>
      </div>
    </Link>
  );
}

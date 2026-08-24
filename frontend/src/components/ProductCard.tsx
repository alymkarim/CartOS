import { Link } from "react-router-dom";
import type { Product } from "../types";

export default function ProductCard({ product }: { product: Product }) {
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
        <p className="text-sm text-text-muted mt-1 line-clamp-2">
          {product.description}
        </p>
        <p className="text-lg font-bold text-text mt-3">{price}</p>
      </div>
    </Link>
  );
}

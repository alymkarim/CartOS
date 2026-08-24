import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../services/api";
import type { Product } from "../types";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    api
      .get<Product[]>("/api/products")
      .then((products) => setProduct(products.find((p) => p.id === id) ?? null))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, [id]);

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
    setIsAdding(true);
    // Cart integration comes in Task 5
    setTimeout(() => setIsAdding(false), 500);
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
    </div>
  );
}

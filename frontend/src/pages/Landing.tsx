import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import type { Product } from "../types";
import ProductCard from "../components/ProductCard";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";

export default function Landing() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api
      .get<Product[]>("/api/products")
      .then((data) => setProducts(data.slice(0, 4)))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-primary/10 via-rose-500/5 to-background py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-text tracking-tight">
            Gear up your workspace
          </h1>
          <p className="text-lg text-text-muted mt-4 max-w-2xl mx-auto">
            Premium developer tools and workspace accessories. Built for people
            who take their setup seriously.
          </p>
          <div className="mt-8 flex items-center justify-center gap-4">
            <Link to="/products">
              <Button size="lg">Browse Products</Button>
            </Link>
            <Link to="/register">
              <Button variant="secondary" size="lg">
                Create Account
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold">Featured Products</h2>
          <Link
            to="/products"
            className="text-sm text-primary hover:text-primary-dark font-medium transition-colors"
          >
            View all →
          </Link>
        </div>

        {isLoading ? (
          <Spinner />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </section>

      {/* Trust Badges */}
      <section className="bg-surface py-16 px-4">
        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-3xl mb-3">🔒</div>
            <h3 className="font-semibold">Secure Checkout</h3>
            <p className="text-sm text-text-muted mt-1">
              Powered by Stripe. Your payment info is never stored.
            </p>
          </div>
          <div>
            <div className="text-3xl mb-3">🚚</div>
            <h3 className="font-semibold">Fast Shipping</h3>
            <p className="text-sm text-text-muted mt-1">
              Free shipping on orders over €50. 2-3 business days.
            </p>
          </div>
          <div>
            <div className="text-3xl mb-3">↩️</div>
            <h3 className="font-semibold">Easy Returns</h3>
            <p className="text-sm text-text-muted mt-1">
              30-day hassle-free returns on all products.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

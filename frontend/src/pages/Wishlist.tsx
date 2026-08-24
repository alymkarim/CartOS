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

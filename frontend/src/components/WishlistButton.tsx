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

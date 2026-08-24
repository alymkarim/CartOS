import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../contexts/CartContext";
import { useAuth } from "../contexts/AuthContext";
import CartItem from "../components/CartItem";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";
import { api } from "../services/api";
import { useState } from "react";

export default function Cart() {
  const { items, total, itemCount, isLoading } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [isCheckingOut, setIsCheckingOut] = useState(false);

  const formattedTotal = new Intl.NumberFormat("en-IE", {
    style: "currency",
    currency: "EUR",
  }).format(total / 100);

  async function handleCheckout() {
    if (!isAuthenticated) {
      navigate("/login?redirect=/cart");
      return;
    }

    setIsCheckingOut(true);
    try {
      const data = await api.post<{ checkout_url: string; session_id: string }>(
        "/api/checkout/cart",
        { items: items.map(({ product_id, quantity }) => ({ product_id, quantity })) }
      );
      window.location.href = data.checkout_url;
    } catch (err) {
      console.error("Checkout failed:", err);
      setIsCheckingOut(false);
    }
  }

  if (isLoading) return <Spinner />;

  if (items.length === 0) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <div className="text-5xl mb-4">🛒</div>
        <h1 className="text-2xl font-bold mb-2">Your cart is empty</h1>
        <p className="text-text-muted mb-6">
          Looks like you haven't added anything yet.
        </p>
        <Link to="/products">
          <Button>Browse Products</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold mb-8">
        Shopping Cart ({itemCount} {itemCount === 1 ? "item" : "items"})
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-surface rounded-xl p-6 shadow-sm">
            {items.map((item) => (
              <CartItem
                key={item.product_id}
                productId={item.product_id}
                quantity={item.quantity}
                product={item.product}
              />
            ))}
          </div>
        </div>

        <div>
          <div className="bg-surface rounded-xl p-6 shadow-sm sticky top-24">
            <h2 className="text-lg font-semibold mb-4">Order Summary</h2>

            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-text-muted">Subtotal</span>
                <span>{formattedTotal}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-muted">Shipping</span>
                <span>Free</span>
              </div>
              <div className="border-t border-black/5 pt-2 mt-2">
                <div className="flex justify-between font-semibold text-base">
                  <span>Total</span>
                  <span>{formattedTotal}</span>
                </div>
              </div>
            </div>

            <Button
              className="w-full mt-6"
              size="lg"
              onClick={handleCheckout}
              isLoading={isCheckingOut}
            >
              {isAuthenticated ? "Proceed to Checkout" : "Sign In to Checkout"}
            </Button>

            <p className="text-xs text-text-muted text-center mt-3">
              Secure checkout powered by Stripe
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

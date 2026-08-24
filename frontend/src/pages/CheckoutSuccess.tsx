import { Link, useSearchParams } from "react-router-dom";
import { useCart } from "../contexts/CartContext";
import { useEffect } from "react";
import Button from "../components/ui/Button";

export default function CheckoutSuccess() {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const { clearCart } = useCart();

  useEffect(() => {
    clearCart();
  }, [clearCart]);

  return (
    <div className="max-w-2xl mx-auto px-4 py-16 text-center">
      <div className="bg-surface rounded-xl p-8 shadow-sm">
        <div className="h-16 w-16 rounded-full bg-success/10 text-success flex items-center justify-center text-3xl mx-auto mb-6">
          ✓
        </div>

        <h1 className="text-2xl font-bold mb-2">Payment Successful!</h1>
        <p className="text-text-muted mb-6">
          Thank you for your order. You'll receive a confirmation email shortly.
        </p>

        {sessionId && (
          <p className="text-xs text-text-muted mb-6">
            Session: {sessionId}
          </p>
        )}

        <div className="flex items-center justify-center gap-4">
          <Link to="/products">
            <Button>Continue Shopping</Button>
          </Link>
          <Link to="/account">
            <Button variant="secondary">View Orders</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}

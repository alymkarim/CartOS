import { Link } from "react-router-dom";
import Button from "../components/ui/Button";

export default function CheckoutCancel() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-16 text-center">
      <div className="bg-surface rounded-xl p-8 shadow-sm">
        <div className="h-16 w-16 rounded-full bg-warning/10 text-warning flex items-center justify-center text-3xl mx-auto mb-6">
          ✕
        </div>

        <h1 className="text-2xl font-bold mb-2">Checkout Cancelled</h1>
        <p className="text-text-muted mb-6">
          No worries — your cart is still saved. You can try again whenever you're ready.
        </p>

        <div className="flex items-center justify-center gap-4">
          <Link to="/cart">
            <Button>Back to Cart</Button>
          </Link>
          <Link to="/products">
            <Button variant="secondary">Continue Shopping</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}

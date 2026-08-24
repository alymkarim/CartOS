import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../services/api";
import type { Order } from "../types";
import Badge from "../components/ui/Badge";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";

export default function OrderDetail() {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) return;
    api
      .get<Order>(`/api/orders/${id}`)
      .then(setOrder)
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  }, [id]);

  if (isLoading) return <Spinner />;

  if (error || !order) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-12 text-center">
        <h1 className="text-2xl font-bold mb-4">Order not found</h1>
        <p className="text-text-muted mb-6">{error}</p>
        <Link to="/account">
          <Button variant="secondary">Back to Account</Button>
        </Link>
      </div>
    );
  }

  const amount = order.amount_total
    ? new Intl.NumberFormat("en-IE", {
        style: "currency",
        currency: "EUR",
      }).format(order.amount_total / 100)
    : "N/A";

  const date = new Date(order.created_at).toLocaleDateString("en-IE", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link
        to="/account"
        className="text-sm text-text-muted hover:text-text transition-colors mb-6 inline-block"
      >
        ← Back to Account
      </Link>

      <div className="bg-surface rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">Order #{order.id}</h1>
          <Badge status={order.payment_status} />
        </div>

        <div className="space-y-4">
          <div className="flex justify-between py-2 border-b border-black/5">
            <span className="text-text-muted">Product</span>
            <span className="font-medium">{order.product_id}</span>
          </div>
          <div className="flex justify-between py-2 border-b border-black/5">
            <span className="text-text-muted">Quantity</span>
            <span>{order.quantity}</span>
          </div>
          <div className="flex justify-between py-2 border-b border-black/5">
            <span className="text-text-muted">Total</span>
            <span className="font-medium">{amount}</span>
          </div>
          <div className="flex justify-between py-2 border-b border-black/5">
            <span className="text-text-muted">Email</span>
            <span>{order.customer_email || "N/A"}</span>
          </div>
          <div className="flex justify-between py-2 border-b border-black/5">
            <span className="text-text-muted">Date</span>
            <span>{date}</span>
          </div>
          <div className="flex justify-between py-2">
            <span className="text-text-muted">Stripe Session</span>
            <span className="text-xs font-mono text-text-muted truncate max-w-[200px]">
              {order.stripe_session_id}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

import { Link } from "react-router-dom";
import type { Order } from "../types";
import Badge from "./ui/Badge";

const statusColors: Record<string, string> = {
  pending: "bg-warning/10 text-warning",
  processing: "bg-blue-500/10 text-blue-500",
  shipped: "bg-indigo-500/10 text-indigo-500",
  delivered: "bg-success/10 text-success",
};

export default function OrderCard({ order }: { order: Order }) {
  const amount = order.amount_total
    ? new Intl.NumberFormat("en-IE", {
        style: "currency",
        currency: "EUR",
      }).format(order.amount_total / 100)
    : "N/A";

  const date = new Date(order.created_at).toLocaleDateString("en-IE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <Link
      to={`/account/orders/${order.id}`}
      className="block bg-surface rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="font-medium">{order.product_id}</p>
          <p className="text-sm text-text-muted">
            Order #{order.id} · {date}
          </p>
        </div>
        <div className="text-right space-y-1">
          <p className="font-medium">{amount}</p>
          <span
            className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
              statusColors[order.status] || "bg-black/5 text-text-muted"
            }`}
          >
            {order.status}
          </span>
          <Badge status={order.payment_status} />
        </div>
      </div>
    </Link>
  );
}

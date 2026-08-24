import { Link } from "react-router-dom";
import type { Order } from "../types";
import Badge from "./ui/Badge";

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
        <div className="text-right">
          <p className="font-medium">{amount}</p>
          <Badge status={order.payment_status} />
        </div>
      </div>
    </Link>
  );
}

import { useEffect, useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { api } from "../services/api";
import type { Order } from "../types";
import OrderCard from "../components/OrderCard";
import Spinner from "../components/ui/Spinner";

export default function Account() {
  const { user } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api
      .get<Order[]>("/api/orders")
      .then(setOrders)
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  const memberSince = user
    ? new Date(user.created_at).toLocaleDateString("en-IE", {
        year: "numeric",
        month: "long",
      })
    : "";

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold mb-8">My Account</h1>

      {/* Profile Card */}
      <div className="bg-surface rounded-xl p-6 shadow-sm mb-8">
        <div className="flex items-center gap-4">
          <div className="h-12 w-12 rounded-full bg-primary text-white flex items-center justify-center text-lg font-medium">
            {user?.email.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="font-medium">{user?.email}</p>
            <p className="text-sm text-text-muted">
              Member since {memberSince}
            </p>
          </div>
        </div>
      </div>

      {/* Order History */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Order History</h2>

        {isLoading ? (
          <Spinner />
        ) : orders.length === 0 ? (
          <div className="bg-surface rounded-xl p-8 shadow-sm text-center">
            <p className="text-text-muted mb-4">You haven't placed any orders yet.</p>
            <a href="/products" className="text-primary hover:text-primary-dark font-medium">
              Browse Products →
            </a>
          </div>
        ) : (
          <div className="space-y-3">
            {orders.map((order) => (
              <OrderCard key={order.id} order={order} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

import type { Product } from "../types";
import { useCart } from "../contexts/CartContext";

interface CartItemProps {
  productId: string;
  quantity: number;
  product: Product;
}

export default function CartItem({ productId, quantity, product }: CartItemProps) {
  const { updateQuantity, removeItem } = useCart();

  const price = new Intl.NumberFormat("en-IE", {
    style: "currency",
    currency: product.currency.toUpperCase(),
  }).format(product.price_cents / 100);

  const subtotal = new Intl.NumberFormat("en-IE", {
    style: "currency",
    currency: product.currency.toUpperCase(),
  }).format((product.price_cents * quantity) / 100);

  return (
    <div className="flex gap-4 py-4 border-b border-black/5 last:border-0">
      <div className="h-20 w-20 rounded-lg overflow-hidden bg-black/5 flex-shrink-0">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-full object-cover"
        />
      </div>

      <div className="flex-1 min-w-0">
        <h3 className="font-medium text-text truncate">{product.name}</h3>
        <p className="text-sm text-text-muted">{price} each</p>

        <div className="flex items-center justify-between mt-2">
          <div className="flex items-center border border-black/10 rounded-lg">
            <button
              onClick={() => updateQuantity(productId, Math.max(1, quantity - 1))}
              className="px-2 py-1 text-sm text-text-muted hover:text-text"
            >
              −
            </button>
            <span className="px-3 py-1 text-sm font-medium">{quantity}</span>
            <button
              onClick={() => updateQuantity(productId, Math.min(10, quantity + 1))}
              className="px-2 py-1 text-sm text-text-muted hover:text-text"
            >
              +
            </button>
          </div>

          <div className="flex items-center gap-4">
            <span className="font-medium">{subtotal}</span>
            <button
              onClick={() => removeItem(productId)}
              className="text-sm text-error hover:text-error/80 transition-colors"
            >
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

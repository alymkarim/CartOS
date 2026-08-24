import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  type ReactNode,
} from "react";
import { api } from "../services/api";
import { useAuth } from "./AuthContext";
import type { Product } from "../types";

interface CartItemData {
  product_id: string;
  quantity: number;
}

interface CartItemWithProduct extends CartItemData {
  product: Product;
}

interface CartContextType {
  items: CartItemWithProduct[];
  isLoading: boolean;
  addItem: (productId: string, quantity?: number) => Promise<void>;
  removeItem: (productId: string) => Promise<void>;
  updateQuantity: (productId: string, quantity: number) => Promise<void>;
  clearCart: () => void;
  total: number;
  itemCount: number;
}

const CartContext = createContext<CartContextType | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItemWithProduct[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    api.get<Product[]>("/api/products").then(setProducts).catch(console.error);
  }, []);

  const loadCart = useCallback(async () => {
    if (!isAuthenticated) {
      const stored = localStorage.getItem("cart");
      if (stored) {
        const parsed: CartItemData[] = JSON.parse(stored);
        const withProducts = parsed
          .map((item) => {
            const product = products.find((p) => p.id === item.product_id);
            return product ? { ...item, product } : null;
          })
          .filter(Boolean) as CartItemWithProduct[];
        setItems(withProducts);
      }
      return;
    }

    setIsLoading(true);
    try {
      const cartItems = await api.get<CartItemData[]>("/api/cart");
      const withProducts = cartItems
        .map((item) => {
          const product = products.find((p) => p.id === item.product_id);
          return product ? { ...item, product } : null;
        })
        .filter(Boolean) as CartItemWithProduct[];
      setItems(withProducts);
    } catch (err) {
      console.error("Failed to load cart:", err);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated, products]);

  useEffect(() => {
    loadCart();
  }, [loadCart]);

  useEffect(() => {
    if (!isAuthenticated) {
      const data = items.map(({ product_id, quantity }) => ({
        product_id,
        quantity,
      }));
      localStorage.setItem("cart", JSON.stringify(data));
    }
  }, [items, isAuthenticated]);

  async function addItem(productId: string, quantity = 1) {
    const product = products.find((p) => p.id === productId);
    if (!product) return;

    if (isAuthenticated) {
      try {
        await api.post("/api/cart", { product_id: productId, quantity });
        await loadCart();
      } catch (err) {
        console.error("Failed to add to cart:", err);
        throw err;
      }
    } else {
      setItems((prev) => {
        const existing = prev.find((i) => i.product_id === productId);
        if (existing) {
          return prev.map((i) =>
            i.product_id === productId
              ? { ...i, quantity: Math.min(10, i.quantity + quantity) }
              : i
          );
        }
        return [...prev, { product_id: productId, quantity, product }];
      });
    }
  }

  async function removeItem(productId: string) {
    if (isAuthenticated) {
      try {
        await api.delete(`/api/cart/${productId}`);
        await loadCart();
      } catch (err) {
        console.error("Failed to remove from cart:", err);
      }
    } else {
      setItems((prev) => prev.filter((i) => i.product_id !== productId));
    }
  }

  async function updateQuantity(productId: string, quantity: number) {
    if (isAuthenticated) {
      try {
        await api.put(`/api/cart/${productId}`, { quantity });
        await loadCart();
      } catch (err) {
        console.error("Failed to update cart:", err);
      }
    } else {
      setItems((prev) =>
        prev.map((i) =>
          i.product_id === productId ? { ...i, quantity } : i
        )
      );
    }
  }

  function clearCart() {
    setItems([]);
    if (!isAuthenticated) {
      localStorage.removeItem("cart");
    }
  }

  const total = items.reduce(
    (sum, item) => sum + item.product.price_cents * item.quantity,
    0
  );

  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        items,
        isLoading,
        addItem,
        removeItem,
        updateQuantity,
        clearCart,
        total,
        itemCount,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}

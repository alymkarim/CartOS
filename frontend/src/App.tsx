import { useEffect, useState } from "react";
import OrdersPage from "./components/OrdersPage";

type Product = {
  id: string;
  name: string;
  description: string;
  price_cents: number;
  currency: string;
  emoji: string;
};

const API_URL = "http://localhost:8000";

function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);
  const [checkoutProductId, setCheckoutProductId] = useState<string | null>(
    null
  );
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProducts() {
      try {
        const response = await fetch(`${API_URL}/api/products`);

        if (!response.ok) {
          throw new Error("Failed to load products.");
        }

        const data: Product[] = await response.json();

        setProducts(data);

        const initialQuantities: Record<string, number> = {};

        data.forEach((product) => {
          initialQuantities[product.id] = 1;
        });

        setQuantities(initialQuantities);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Unable to load products."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, []);

  function updateQuantity(productId: string, quantity: number) {
    setQuantities((current) => ({
      ...current,
      [productId]: Math.max(1, quantity),
    }));
  }

  async function handleBuy(productId: string) {
    setError("");
    setCheckoutProductId(productId);

    try {
      const response = await fetch(`${API_URL}/api/checkout/session`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          product_id: productId,
          quantity: quantities[productId] ?? 1,
        }),
      });

      if (!response.ok) {
        throw new Error("Unable to create checkout session.");
      }

      const data = await response.json();

      window.location.href = data.checkout_url;
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Checkout could not be created."
      );
      setCheckoutProductId(null);
    }
  }

  if (loading) {
    return <main>Loading products...</main>;
  }

  return (
    <main className="page">
      <header>
        <h1>PayForge</h1>
        <p>Secure test payments powered by Stripe.</p>
      </header>

      {error && <p className="error">{error}</p>}

      <section className="product-grid">
        {products.map((product) => (
          <article className="product-card" key={product.id}>
            <div className="emoji">{product.emoji}</div>

            <h2>{product.name}</h2>

            <p>{product.description}</p>

            <strong>
              {(product.price_cents / 100).toLocaleString("en-IE", {
                style: "currency",
                currency: product.currency.toUpperCase(),
              })}
            </strong>

            <label>
              Quantity
              <input
                type="number"
                min="1"
                max="10"
                value={quantities[product.id] ?? 1}
                onChange={(event) =>
                  updateQuantity(product.id, Number(event.target.value))
                }
              />
            </label>

            <button
              onClick={() => handleBuy(product.id)}
              disabled={checkoutProductId === product.id}
            >
              {checkoutProductId === product.id
                ? "Creating checkout..."
                : "Buy now"}
            </button>
          </article>
        ))}
      </section>

      <hr style={{ margin: "3rem 0" }} />

      <OrdersPage />
    </main>
  );
}

export default App;
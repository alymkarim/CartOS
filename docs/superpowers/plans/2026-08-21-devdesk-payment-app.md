# DevDesk Payment App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the existing PayForge app into a polished, portfolio-worthy e-commerce store with Tailwind CSS, React Router, full auth flow, cart system, and expanded product catalog.

**Architecture:** React frontend with Tailwind CSS v4 + React Router v7, communicating with FastAPI backend via REST API. Auth uses JWT stored in localStorage with React Context for state management. Cart uses both localStorage (guest) and DB-backed API (logged-in user).

**Tech Stack:** React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7, FastAPI, SQLAlchemy, Stripe, PostgreSQL

## Global Constraints

- All frontend styling uses Tailwind CSS v4 utility classes — no custom CSS files except `index.css` for Tailwind directives
- All pages use React Router v7 for navigation — no manual URL manipulation
- Auth tokens stored in localStorage, attached via Authorization header
- Backend uses SQLAlchemy models with PostgreSQL
- Stripe integration uses test mode (`sk_test_` prefix required)
- Product images use placeholder URLs from picsum.photos or unsplash.com
- Color palette: coral primary (`#f97316`), teal secondary (`#14b8a6`), warm background (`#fffbf5`)
- Font: Inter from Google Fonts
- All API calls go through a centralized `api.ts` service with auth headers

---

## Branch Strategy

Follow the existing repo pattern: feature branches → PR merges to main.

| Branch | Tasks | Description |
|---|---|---|
| `feature/tailwind-setup` | Task 1 | Tailwind CSS, React Router, layout shell |
| `feature/auth-pages` | Task 2, 3 | Auth context, login, register, forgot/reset password |
| `feature/product-catalog` | Task 4 | Expanded products, Landing, Catalog, Detail pages |
| `feature/cart-system` | Task 5 | Cart API, CartContext, cart page, checkout integration |
| `feature/account-orders` | Task 6 | Account page, order detail, user-scoped orders, webhook fix |
| `feature/password-reset` | Task 7 | Backend password reset endpoints, validation |
| `feature/polish` | Task 8 | Responsive, error boundary, loading states |

Each branch is created from `main`, developed, committed, then merged back via PR (or `git merge`). This matches the existing history pattern (feature/backend-setup, feature/jwt-auth, frontend, etc.).

**Commit style:** Use the same style as existing commits — short, lowercase, descriptive (e.g., "add auth", "frontend changes", "work on orders api").

---

## File Structure

### Frontend (New/Modified)

```
frontend/src/
├── main.tsx                    # Add Router + providers
├── App.tsx                     # Route definitions (rewrite)
├── index.css                   # Tailwind directives (rewrite)
├── types/
│   └── index.ts                # TypeScript types (new)
├── contexts/
│   ├── AuthContext.tsx          # Auth state management (new)
│   └── CartContext.tsx          # Cart state management (new)
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx          # Sticky nav (new)
│   │   ├── Footer.tsx          # Footer (new)
│   │   └── ProtectedRoute.tsx  # Auth guard (new)
│   ├── ui/
│   │   ├── Button.tsx          # Reusable button (new)
│   │   ├── Badge.tsx           # Status badges (new)
│   │   ├── Input.tsx           # Form input (new)
│   │   ├── Spinner.tsx         # Loading spinner (new)
│   │   └── PasswordStrength.tsx # Password meter (new)
│   ├── ProductCard.tsx         # Product card (new)
│   ├── CartItem.tsx            # Cart item row (new)
│   └── OrderCard.tsx           # Order summary (new)
├── pages/
│   ├── Landing.tsx             # Hero + featured (new)
│   ├── ProductCatalog.tsx      # Full grid (new)
│   ├── ProductDetail.tsx       # Single product (new)
│   ├── Cart.tsx                # Shopping cart (new)
│   ├── CheckoutSuccess.tsx     # Success page (new)
│   ├── CheckoutCancel.tsx      # Cancel page (new)
│   ├── Login.tsx               # Sign in (new)
│   ├── Register.tsx            # Create account (new)
│   ├── ForgotPassword.tsx      # Forgot password (new)
│   ├── ResetPassword.tsx       # Reset password (new)
│   ├── Account.tsx             # Profile + orders (new)
│   └── OrderDetail.tsx         # Single order (new)
├── services/
│   └── api.ts                  # API client (rewrite)
```

### Backend (New/Modified)

```
backend/app/
├── models.py                   # Add CartItem, PasswordReset models
├── schemas.py                  # Add CartItem, PasswordReset schemas
├── product.py                  # Expand to 8 products + image_url
├── security.py                 # Add password validation
├── dependencies.py             # No changes
├── routers/
│   ├── auth.py                 # Add forgot-password, reset-password
│   ├── cart.py                 # New: Cart CRUD endpoints
│   ├── checkout.py             # Add cart-based checkout
│   ├── orders.py               # Fix: user-scoped queries
│   ├── products.py             # No changes
│   └── webhook.py              # Fix: indentation bug
```

---

## Task 1: Frontend Foundation — Tailwind + React Router + Layout
**Branch:** `feature/tailwind-setup`

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/index.html`
- Create: `frontend/src/types/index.ts`
- Rewrite: `frontend/src/index.css`
- Rewrite: `frontend/src/main.tsx`
- Rewrite: `frontend/src/App.tsx`
- Create: `frontend/src/components/layout/Navbar.tsx`
- Create: `frontend/src/components/layout/Footer.tsx`
- Create: `frontend/src/components/ui/Button.tsx`
- Create: `frontend/src/components/ui/Spinner.tsx`

**Interfaces:**
- Produces: App shell with Navbar + Footer, route structure, Tailwind config
- Consumes: None (foundation task)

- [ ] **Step 1: Install dependencies**

```bash
cd frontend
npm install react-router-dom@7
npm install -D tailwindcss @tailwindcss/vite
```

- [ ] **Step 2: Configure Tailwind in vite.config.ts**

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": "/src",
    },
  },
});
```

- [ ] **Step 3: Rewrite index.css with Tailwind directives**

```css
@import "tailwindcss";

@theme {
  --color-primary: #f97316;
  --color-primary-dark: #ea580c;
  --color-secondary: #14b8a6;
  --color-background: #fffbf5;
  --color-surface: #ffffff;
  --color-text: #1c1917;
  --color-text-muted: #78716c;
  --color-success: #10b981;
  --color-error: #ef4444;
  --color-warning: #f59e0b;
}

body {
  margin: 0;
  font-family: "Inter", sans-serif;
  background-color: var(--color-background);
  color: var(--color-text);
  -webkit-font-smoothing: antialiased;
}

* {
  box-sizing: border-box;
}
```

- [ ] **Step 4: Update index.html with Inter font**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <title>DevDesk — Developer Workspace Gear</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **Step 5: Create TypeScript types**

```typescript
// frontend/src/types/index.ts

export interface User {
  id: number;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price_cents: number;
  currency: string;
  emoji: string;
  image_url: string;
}

export interface CartItem {
  product_id: string;
  quantity: number;
}

export interface Order {
  id: number;
  stripe_session_id: string;
  product_id: string;
  quantity: number;
  payment_status: string;
  amount_total: number | null;
  customer_email: string | null;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
```

- [ ] **Step 6: Create Button component**

```typescript
// frontend/src/components/ui/Button.tsx

import { type ButtonHTMLAttributes, type ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  children: ReactNode;
}

export default function Button({
  variant = "primary",
  size = "md",
  isLoading = false,
  children,
  className = "",
  disabled,
  ...props
}: ButtonProps) {
  const base =
    "inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:opacity-50 disabled:cursor-not-allowed";

  const variants = {
    primary:
      "bg-gradient-to-r from-primary to-rose-500 text-white hover:shadow-lg hover:shadow-primary/25",
    secondary:
      "border-2 border-primary text-primary hover:bg-primary hover:text-white",
    ghost: "text-text-muted hover:text-text hover:bg-black/5",
  };

  const sizes = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-5 py-2.5 text-sm",
    lg: "px-6 py-3 text-base",
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
          />
        </svg>
      )}
      {children}
    </button>
  );
}
```

- [ ] **Step 7: Create Spinner component**

```typescript
// frontend/src/components/ui/Spinner.tsx

export default function Spinner({ size = "md" }: { size?: "sm" | "md" | "lg" }) {
  const sizes = {
    sm: "h-4 w-4",
    md: "h-8 w-8",
    lg: "h-12 w-12",
  };

  return (
    <div className="flex items-center justify-center py-12">
      <div
        className={`${sizes[size]} animate-spin rounded-full border-2 border-text-muted border-t-primary`}
      />
    </div>
  );
}
```

- [ ] **Step 8: Create Navbar component**

```typescript
// frontend/src/components/layout/Navbar.tsx

import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-surface/80 backdrop-blur-md border-b border-black/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="text-xl font-bold text-text">
            DevDesk
          </Link>

          <div className="hidden md:flex items-center gap-8">
            <Link
              to="/products"
              className="text-text-muted hover:text-text transition-colors"
            >
              Products
            </Link>
          </div>

          <div className="flex items-center gap-4">
            <Link
              to="/cart"
              className="relative p-2 text-text-muted hover:text-text transition-colors"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
                />
              </svg>
            </Link>

            <Link
              to="/login"
              className="text-sm font-medium text-text-muted hover:text-text transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
```

- [ ] **Step 9: Create Footer component**

```typescript
// frontend/src/components/layout/Footer.tsx

export default function Footer() {
  return (
    <footer className="bg-text text-white py-12 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">DevDesk</h3>
            <p className="text-white/60 text-sm">
              Premium gear for developers who care about their workspace.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold mb-4 uppercase tracking-wider text-white/40">
              Shop
            </h4>
            <ul className="space-y-2 text-sm text-white/60">
              <li><a href="/products" className="hover:text-white transition-colors">All Products</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold mb-4 uppercase tracking-wider text-white/40">
              Account
            </h4>
            <ul className="space-y-2 text-sm text-white/60">
              <li><a href="/login" className="hover:text-white transition-colors">Sign In</a></li>
              <li><a href="/register" className="hover:text-white transition-colors">Create Account</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-white/10 mt-8 pt-8 text-center text-sm text-white/40">
          Built with FastAPI, React & Stripe
        </div>
      </div>
    </footer>
  );
}
```

- [ ] **Step 10: Rewrite main.tsx with Router**

```typescript
// frontend/src/main.tsx

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
```

- [ ] **Step 11: Rewrite App.tsx with routes**

```typescript
// frontend/src/App.tsx

import { Routes, Route } from "react-router-dom";
import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";
import Landing from "./pages/Landing";
import ProductCatalog from "./pages/ProductCatalog";
import ProductDetail from "./pages/ProductDetail";
import Cart from "./pages/Cart";
import CheckoutSuccess from "./pages/CheckoutSuccess";
import CheckoutCancel from "./pages/CheckoutCancel";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Account from "./pages/Account";
import OrderDetail from "./pages/OrderDetail";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/products" element={<ProductCatalog />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/checkout/success" element={<CheckoutSuccess />} />
          <Route path="/checkout/cancel" element={<CheckoutCancel />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/account" element={<Account />} />
          <Route path="/account/orders/:id" element={<OrderDetail />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
```

- [ ] **Step 12: Create placeholder pages (stubs)**

Create all page files as stubs so the app compiles:

```typescript
// frontend/src/pages/Landing.tsx
export default function Landing() {
  return <div className="max-w-7xl mx-auto px-4 py-12"><h1>Landing</h1></div>;
}
```

Repeat for all 12 pages with the same pattern.

- [ ] **Step 13: Delete unused files**

Delete:
- `frontend/src/App.css`
- `frontend/src/components/OrdersPage.tsx`
- `frontend/src/components/CheckoutButton.tsx`
- `frontend/src/components/ProductCard.tsx` (empty)
- `frontend/src/components/Navbar.tsx` (empty, replaced by layout/Navbar)
- `frontend/src/pages/Home.tsx` (empty, replaced by Landing)
- `frontend/src/pages/Success.tsx` (empty, replaced by CheckoutSuccess)
- `frontend/src/pages/Cancel.tsx` (empty, replaced by CheckoutCancel)

- [ ] **Step 14: Verify app compiles**

```bash
cd frontend && npm run dev
```

Open http://localhost:5173 — should see Navbar + Footer with stub pages routing correctly.

- [ ] **Step 15: Commit and merge**

```bash
git add frontend/
git commit -m "set up tailwind, react router, layout shell, and page stubs"

# Merge to main
git checkout main
git merge feature/tailwind-setup
```

---

## Task 2: API Client + Auth Context
**Branch:** `feature/auth-pages`

**Files:**
- Rewrite: `frontend/src/services/api.ts`
- Create: `frontend/src/contexts/AuthContext.tsx`
- Modify: `frontend/src/main.tsx` (add AuthProvider)
- Create: `frontend/src/components/layout/ProtectedRoute.tsx`
- Create: `frontend/src/components/ui/Input.tsx`
- Create: `frontend/src/components/ui/PasswordStrength.tsx`

**Interfaces:**
- Produces: `AuthContext` with `{ user, token, isAuthenticated, isLoading, login(), register(), logout(), forgotPassword(), resetPassword() }`
- Consumes: Backend `/api/auth/*` endpoints

- [ ] **Step 1: Rewrite api.ts**

```typescript
// frontend/src/services/api.ts

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private getToken(): string | null {
    return localStorage.getItem("token");
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Request failed with status ${response.status}`);
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint);
  }

  async post<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async put<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "DELETE" });
  }

  async postForm<T>(endpoint: string, body: URLSearchParams): Promise<T> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      "Content-Type": "application/x-www-form-urlencoded",
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: "POST",
      headers,
      body: body.toString(),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Request failed with status ${response.status}`);
    }

    return response.json();
  }
}

export const api = new ApiClient(API_URL);
```

- [ ] **Step 2: Create Input component**

```typescript
// frontend/src/components/ui/Input.tsx

import { type InputHTMLAttributes, type ReactNode } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  icon?: ReactNode;
}

export default function Input({
  label,
  error,
  icon,
  className = "",
  id,
  ...props
}: InputProps) {
  const inputId = id || label.toLowerCase().replace(/\s+/g, "-");

  return (
    <div className="space-y-1">
      <label
        htmlFor={inputId}
        className="block text-sm font-medium text-text"
      >
        {label}
      </label>
      <div className="relative">
        {icon && (
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted">
            {icon}
          </div>
        )}
        <input
          id={inputId}
          className={`w-full rounded-lg border ${
            error ? "border-error" : "border-black/10"
          } bg-surface px-4 py-2.5 text-sm text-text placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors ${
            icon ? "pl-10" : ""
          } ${className}`}
          {...props}
        />
      </div>
      {error && <p className="text-xs text-error">{error}</p>}
    </div>
  );
}
```

- [ ] **Step 3: Create PasswordStrength component**

```typescript
// frontend/src/components/ui/PasswordStrength.tsx

interface PasswordStrengthProps {
  password: string;
}

export default function PasswordStrength({ password }: PasswordStrengthProps) {
  const checks = [
    { label: "At least 8 characters", met: password.length >= 8 },
    { label: "One uppercase letter", met: /[A-Z]/.test(password) },
    { label: "One lowercase letter", met: /[a-z]/.test(password) },
    { label: "One number", met: /\d/.test(password) },
  ];

  const score = checks.filter((c) => c.met).length;

  if (!password) return null;

  return (
    <div className="space-y-2">
      <div className="flex gap-1">
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className={`h-1 flex-1 rounded-full transition-colors ${
              i <= score
                ? score <= 1
                  ? "bg-error"
                  : score <= 2
                  ? "bg-warning"
                  : "bg-success"
                : "bg-black/10"
            }`}
          />
        ))}
      </div>
      <ul className="space-y-1">
        {checks.map((check) => (
          <li
            key={check.label}
            className={`text-xs ${
              check.met ? "text-success" : "text-text-muted"
            }`}
          >
            {check.met ? "✓" : "○"} {check.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

- [ ] **Step 4: Create AuthContext**

```typescript
// frontend/src/contexts/AuthContext.tsx

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { api } from "../services/api";
import type { User, AuthResponse } from "../types";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  forgotPassword: (email: string) => Promise<string>;
  resetPassword: (token: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (token) {
      api
        .get<User>("/api/auth/me")
        .then(setUser)
        .catch(() => {
          localStorage.removeItem("token");
          setToken(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [token]);

  async function login(email: string, password: string) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const data = await api.postForm<AuthResponse>("/api/auth/login", formData);
    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);
    const userData = await api.get<User>("/api/auth/me");
    setUser(userData);
  }

  async function register(email: string, password: string) {
    await api.post("/api/auth/register", { email, password });
    await login(email, password);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }

  async function forgotPassword(email: string) {
    const data = await api.post<{ token: string }>("/api/auth/forgot-password", { email });
    return data.token;
  }

  async function resetPassword(resetToken: string, password: string) {
    await api.post("/api/auth/reset-password", { token: resetToken, password });
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        forgotPassword,
        resetPassword,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
```

- [ ] **Step 5: Add AuthProvider to main.tsx**

```typescript
// frontend/src/main.tsx

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import App from "./App";
import "./index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
```

- [ ] **Step 6: Create ProtectedRoute component**

```typescript
// frontend/src/components/layout/ProtectedRoute.tsx

import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import Spinner from "../ui/Spinner";
import type { ReactNode } from "react";

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <Spinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to={`/login?redirect=${location.pathname}`} replace />;
  }

  return <>{children}</>;
}
```

- [ ] **Step 7: Update App.tsx to use ProtectedRoute**

Update the `/account` routes in App.tsx:

```typescript
import ProtectedRoute from "./components/layout/ProtectedRoute";

// In the Routes:
<Route path="/account" element={<ProtectedRoute><Account /></ProtectedRoute>} />
<Route path="/account/orders/:id" element={<ProtectedRoute><OrderDetail /></ProtectedRoute>} />
```

- [ ] **Step 8: Verify auth compiles**

```bash
cd frontend && npm run build
```

Fix any TypeScript errors.

- [ ] **Step 9: Commit**

```bash
git add frontend/
git commit -m "add api client, auth context, protected routes, and ui components"
```

---

## Task 3: Auth Pages — Login, Register, Forgot/Reset Password
**Branch:** `feature/auth-pages` (continued from Task 2)

**Files:**
- Rewrite: `frontend/src/pages/Login.tsx`
- Rewrite: `frontend/src/pages/Register.tsx`
- Create: `frontend/src/pages/ForgotPassword.tsx`
- Create: `frontend/src/pages/ResetPassword.tsx`

**Interfaces:**
- Consumes: `useAuth()` hook with `login()`, `register()`, `forgotPassword()`, `resetPassword()`
- Produces: Working auth flow with redirects

- [ ] **Step 1: Implement Login page**

```typescript
// frontend/src/pages/Login.tsx

import { useState, type FormEvent } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const redirect = searchParams.get("redirect") || "/account";

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await login(email, password);
      navigate(redirect, { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold">Welcome back</h1>
          <p className="text-text-muted mt-2">Sign in to your DevDesk account</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-surface rounded-xl p-6 shadow-sm space-y-4">
          {error && (
            <div className="bg-error/10 text-error text-sm p-3 rounded-lg">
              {error}
            </div>
          )}

          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />

          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />

          <div className="flex items-center justify-end">
            <Link
              to="/forgot-password"
              className="text-sm text-primary hover:text-primary-dark transition-colors"
            >
              Forgot password?
            </Link>
          </div>

          <Button type="submit" isLoading={isLoading} className="w-full">
            Sign In
          </Button>
        </form>

        <p className="text-center text-sm text-text-muted mt-6">
          Don't have an account?{" "}
          <Link to="/register" className="text-primary hover:text-primary-dark font-medium transition-colors">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Implement Register page**

```typescript
// frontend/src/pages/Register.tsx

import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import PasswordStrength from "../components/ui/PasswordStrength";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    setIsLoading(true);

    try {
      await register(email, password);
      navigate("/account", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold">Create your account</h1>
          <p className="text-text-muted mt-2">Start shopping at DevDesk</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-surface rounded-xl p-6 shadow-sm space-y-4">
          {error && (
            <div className="bg-error/10 text-error text-sm p-3 rounded-lg">
              {error}
            </div>
          )}

          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />

          <div className="space-y-1">
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a password"
              required
            />
            <PasswordStrength password={password} />
          </div>

          <Input
            label="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm your password"
            required
          />

          <Button type="submit" isLoading={isLoading} className="w-full">
            Create Account
          </Button>
        </form>

        <p className="text-center text-sm text-text-muted mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-primary hover:text-primary-dark font-medium transition-colors">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Implement ForgotPassword page**

```typescript
// frontend/src/pages/ForgotPassword.tsx

import { useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState("");
  const { forgotPassword } = useAuth();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const resetToken = await forgotPassword(email);
      setToken(resetToken);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setIsLoading(false);
    }
  }

  if (token) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center px-4">
        <div className="w-full max-w-md text-center">
          <div className="bg-surface rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-bold mb-4">Reset link generated</h2>
            <p className="text-text-muted text-sm mb-6">
              In a real app, this would be emailed. For this demo, use the link below:
            </p>
            <a
              href={`/reset-password?token=${token}`}
              className="text-primary hover:text-primary-dark underline break-all text-sm"
            >
              /reset-password?token={token}
            </a>
            <div className="mt-6">
              <Link to="/login">
                <Button variant="secondary" className="w-full">
                  Back to Login
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold">Forgot your password?</h1>
          <p className="text-text-muted mt-2">
            Enter your email and we'll generate a reset link
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bg-surface rounded-xl p-6 shadow-sm space-y-4">
          {error && (
            <div className="bg-error/10 text-error text-sm p-3 rounded-lg">
              {error}
            </div>
          )}

          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />

          <Button type="submit" isLoading={isLoading} className="w-full">
            Generate Reset Link
          </Button>
        </form>

        <p className="text-center text-sm text-text-muted mt-6">
          Remember your password?{" "}
          <Link to="/login" className="text-primary hover:text-primary-dark font-medium transition-colors">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Implement ResetPassword page**

```typescript
// frontend/src/pages/ResetPassword.tsx

import { useState, type FormEvent } from "react";
import { Link, useSearchParams, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import PasswordStrength from "../components/ui/PasswordStrength";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const { resetPassword } = useAuth();
  const navigate = useNavigate();

  if (!token) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center px-4">
        <div className="w-full max-w-md text-center">
          <h1 className="text-2xl font-bold mb-4">Invalid reset link</h1>
          <p className="text-text-muted mb-6">This password reset link is invalid or has expired.</p>
          <Link to="/forgot-password">
            <Button>Request a new link</Button>
          </Link>
        </div>
      </div>
    );
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    setIsLoading(true);

    try {
      await resetPassword(token, password);
      setIsSuccess(true);
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Reset failed");
    } finally {
      setIsLoading(false);
    }
  }

  if (isSuccess) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center px-4">
        <div className="w-full max-w-md text-center">
          <div className="bg-surface rounded-xl p-6 shadow-sm">
            <div className="text-success text-4xl mb-4">✓</div>
            <h2 className="text-xl font-bold mb-2">Password reset successful</h2>
            <p className="text-text-muted">Redirecting to login...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold">Set new password</h1>
          <p className="text-text-muted mt-2">Enter your new password below</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-surface rounded-xl p-6 shadow-sm space-y-4">
          {error && (
            <div className="bg-error/10 text-error text-sm p-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="space-y-1">
            <Input
              label="New Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter new password"
              required
            />
            <PasswordStrength password={password} />
          </div>

          <Input
            label="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm new password"
            required
          />

          <Button type="submit" isLoading={isLoading} className="w-full">
            Reset Password
          </Button>
        </form>
      </div>
    </div>
  );
}
```

- [ ] **Step 5: Verify auth pages compile**

```bash
cd frontend && npm run build
```

- [ ] **Step 6: Commit and merge**

```bash
git add frontend/
git commit -m "add login, register, forgot password, and reset password pages"

# Merge to main
git checkout main
git merge feature/auth-pages
```

---

## Task 4: Product Data + Product Pages
**Branch:** `feature/product-catalog`

**Files:**
- Modify: `backend/app/product.py` (expand to 8 products + image_url)
- Modify: `backend/app/schemas.py` (add image_url to Product)
- Create: `frontend/src/components/ProductCard.tsx`
- Rewrite: `frontend/src/pages/Landing.tsx`
- Rewrite: `frontend/src/pages/ProductCatalog.tsx`
- Rewrite: `frontend/src/pages/ProductDetail.tsx`

**Interfaces:**
- Consumes: `GET /api/products`, `Product` type
- Produces: Landing page, product grid, product detail page

- [ ] **Step 1: Update Product schema with image_url**

```python
# backend/app/schemas.py — add image_url field to Product class

class Product(BaseModel):
    id: str
    name: str
    description: str
    price_cents: int = Field(gt=0)
    currency: str = "eur"
    emoji: str
    image_url: str
```

- [ ] **Step 2: Expand product catalog**

```python
# backend/app/product.py

from app.schemas import Product

PRODUCTS: dict[str, Product] = {
    "desk-lamp": Product(
        id="desk-lamp",
        name="Focus Desk Lamp",
        description="Adjustable LED lamp with warm and cool color temperature modes. Perfect for late-night coding sessions.",
        price_cents=2999,
        currency="eur",
        emoji="💡",
        image_url="https://picsum.photos/seed/desk-lamp/400/400",
    ),
    "mechanical-keyboard": Product(
        id="mechanical-keyboard",
        name="MX Artisan Keyboard",
        description="Hot-swappable mechanical keyboard with PBT keycaps and per-key RGB lighting. Tactile switches included.",
        price_cents=7999,
        currency="eur",
        emoji="⌨️",
        image_url="https://picsum.photos/seed/keyboard/400/400",
    ),
    "developer-mug": Product(
        id="developer-mug",
        name="Debug Fuel Mug",
        description="12oz ceramic mug with a matte finish. Dishwasher and microwave safe. Holds enough coffee for a sprint.",
        price_cents=1499,
        currency="eur",
        emoji="☕",
        image_url="https://picsum.photos/seed/mug/400/400",
    ),
    "ultrawide-monitor": Product(
        id="ultrawide-monitor",
        name='UltraWide 34"',
        description="3440x1440 curved IPS display with USB-C power delivery. 100Hz refresh rate, HDR400.",
        price_cents=44999,
        currency="eur",
        emoji="🖥️",
        image_url="https://picsum.photos/seed/monitor/400/400",
    ),
    "webcam-pro": Product(
        id="webcam-pro",
        name="StreamCam Pro",
        description="4K webcam with auto-light correction and noise-cancelling dual microphones. USB-C connection.",
        price_cents=8999,
        currency="eur",
        emoji="📷",
        image_url="https://picsum.photos/seed/webcam/400/400",
    ),
    "desk-mat": Product(
        id="desk-mat",
        name="Felt Desk Mat",
        description="Premium wool felt desk mat, 900x400mm. Includes genuine leather strap for easy rolling and storage.",
        price_cents=3499,
        currency="eur",
        emoji="🖱️",
        image_url="https://picsum.photos/seed/deskmat/400/400",
    ),
    "noise-cancelling": Product(
        id="noise-cancelling",
        name="QuietPro Headset",
        description="Active noise cancelling over-ear headphones with 40-hour battery life. Multipoint Bluetooth connectivity.",
        price_cents=19999,
        currency="eur",
        emoji="🎧",
        image_url="https://picsum.photos/seed/headset/400/400",
    ),
    "usb-c-hub": Product(
        id="usb-c-hub",
        name="Thunderbolt Hub",
        description="7-in-1 USB-C hub with dual HDMI 4K output, 100W power delivery, and gigabit ethernet.",
        price_cents=6999,
        currency="eur",
        emoji="🔌",
        image_url="https://picsum.photos/seed/usbhub/400/400",
    ),
}


def list_products() -> list[Product]:
    return list(PRODUCTS.values())


def get_product(product_id: str) -> Product | None:
    return PRODUCTS.get(product_id)
```

- [ ] **Step 3: Create ProductCard component**

```typescript
// frontend/src/components/ProductCard.tsx

import { Link } from "react-router-dom";
import type { Product } from "../types";

export default function ProductCard({ product }: { product: Product }) {
  const price = new Intl.NumberFormat("en-IE", {
    style: "currency",
    currency: product.currency.toUpperCase(),
  }).format(product.price_cents / 100);

  return (
    <Link
      to={`/products/${product.id}`}
      className="group bg-surface rounded-xl overflow-hidden shadow-sm hover:shadow-lg hover:shadow-primary/10 transition-all duration-300 hover:-translate-y-1"
    >
      <div className="aspect-square overflow-hidden bg-black/5">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-text group-hover:text-primary transition-colors">
          {product.name}
        </h3>
        <p className="text-sm text-text-muted mt-1 line-clamp-2">
          {product.description}
        </p>
        <p className="text-lg font-bold text-text mt-3">{price}</p>
      </div>
    </Link>
  );
}
```

- [ ] **Step 4: Implement Landing page**

```typescript
// frontend/src/pages/Landing.tsx

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api";
import type { Product } from "../types";
import ProductCard from "../components/ProductCard";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";

export default function Landing() {
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api
      .get<Product[]>("/api/products")
      .then((data) => setProducts(data.slice(0, 3)))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-primary/10 via-rose-500/5 to-background py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-text tracking-tight">
            Gear up your workspace
          </h1>
          <p className="text-lg text-text-muted mt-4 max-w-2xl mx-auto">
            Premium developer tools and workspace accessories. Built for people
            who take their setup seriously.
          </p>
          <div className="mt-8 flex items-center justify-center gap-4">
            <Link to="/products">
              <Button size="lg">Browse Products</Button>
            </Link>
            <Link to="/register">
              <Button variant="secondary" size="lg">
                Create Account
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold">Featured Products</h2>
          <Link
            to="/products"
            className="text-sm text-primary hover:text-primary-dark font-medium transition-colors"
          >
            View all →
          </Link>
        </div>

        {isLoading ? (
          <Spinner />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </section>

      {/* Trust Badges */}
      <section className="bg-surface py-16 px-4">
        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-3xl mb-3">🔒</div>
            <h3 className="font-semibold">Secure Checkout</h3>
            <p className="text-sm text-text-muted mt-1">
              Powered by Stripe. Your payment info is never stored.
            </p>
          </div>
          <div>
            <div className="text-3xl mb-3">🚚</div>
            <h3 className="font-semibold">Fast Shipping</h3>
            <p className="text-sm text-text-muted mt-1">
              Free shipping on orders over €50. 2-3 business days.
            </p>
          </div>
          <div>
            <div className="text-3xl mb-3">↩️</div>
            <h3 className="font-semibold">Easy Returns</h3>
            <p className="text-sm text-text-muted mt-1">
              30-day hassle-free returns on all products.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
```

- [ ] **Step 5: Implement ProductCatalog page**

```typescript
// frontend/src/pages/ProductCatalog.tsx

import { useEffect, useState } from "react";
import { api } from "../services/api";
import type { Product } from "../types";
import ProductCard from "../components/ProductCard";
import Spinner from "../components/ui/Spinner";

export default function ProductCatalog() {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api
      .get<Product[]>("/api/products")
      .then(setProducts)
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  const filtered = products.filter(
    (p) =>
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">All Products</h1>
        <p className="text-text-muted mt-2">
          Everything you need for the perfect developer workspace.
        </p>
      </div>

      <div className="mb-8">
        <input
          type="text"
          placeholder="Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full max-w-md rounded-lg border border-black/10 bg-surface px-4 py-2.5 text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
        />
      </div>

      {isLoading ? (
        <Spinner />
      ) : filtered.length === 0 ? (
        <p className="text-text-muted text-center py-12">
          No products found matching "{search}"
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filtered.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 6: Implement ProductDetail page**

```typescript
// frontend/src/pages/ProductDetail.tsx

import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../services/api";
import type { Product } from "../types";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    api
      .get<Product[]>("/api/products")
      .then((products) => setProduct(products.find((p) => p.id === id) ?? null))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, [id]);

  if (isLoading) return <Spinner />;

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center">
        <h1 className="text-2xl font-bold mb-4">Product not found</h1>
        <Link to="/products">
          <Button variant="secondary">Back to Products</Button>
        </Link>
      </div>
    );
  }

  const price = new Intl.NumberFormat("en-IE", {
    style: "currency",
    currency: product.currency.toUpperCase(),
  }).format(product.price_cents / 100);

  async function handleAddToCart() {
    setIsAdding(true);
    // Cart integration comes in Task 5
    setTimeout(() => setIsAdding(false), 500);
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <Link
        to="/products"
        className="text-sm text-text-muted hover:text-text transition-colors mb-6 inline-block"
      >
        ← Back to Products
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div className="aspect-square rounded-xl overflow-hidden bg-black/5">
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover"
          />
        </div>

        <div>
          <h1 className="text-3xl font-bold">{product.name}</h1>
          <p className="text-3xl font-bold text-primary mt-2">{price}</p>
          <p className="text-text-muted mt-4 leading-relaxed">
            {product.description}
          </p>

          <div className="mt-8 space-y-4">
            <div className="flex items-center gap-4">
              <label className="text-sm font-medium">Quantity</label>
              <div className="flex items-center border border-black/10 rounded-lg">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="px-3 py-2 text-text-muted hover:text-text transition-colors"
                >
                  −
                </button>
                <span className="px-4 py-2 text-sm font-medium">{quantity}</span>
                <button
                  onClick={() => setQuantity(Math.min(10, quantity + 1))}
                  className="px-3 py-2 text-text-muted hover:text-text transition-colors"
                >
                  +
                </button>
              </div>
            </div>

            <Button
              size="lg"
              className="w-full"
              isLoading={isAdding}
              onClick={handleAddToCart}
            >
              Add to Cart
            </Button>

            <p className="text-xs text-text-muted text-center">
              Secure checkout powered by Stripe
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 7: Start backend and verify products API**

```bash
cd backend
python -m uvicorn main:app --reload
```

Test: `curl http://localhost:8000/api/products` — should return 8 products with image_url.

- [ ] **Step 8: Verify frontend compiles and pages work**

```bash
cd frontend && npm run dev
```

Visit:
- http://localhost:5173/ — Landing with hero + 3 featured products
- http://localhost:5173/products — Full grid of 8 products
- http://localhost:5173/products/desk-lamp — Product detail page

- [ ] **Step 9: Commit and merge**

```bash
git add backend/app/product.py backend/app/schemas.py frontend/
git commit -m "expand product catalog to 8 products with images and product pages"

# Merge to main
git checkout main
git merge feature/product-catalog
```

---

## Task 5: Cart System — Context + Pages + Backend API
**Branch:** `feature/cart-system`

**Files:**
- Create: `frontend/src/contexts/CartContext.tsx`
- Create: `frontend/src/components/CartItem.tsx`
- Rewrite: `frontend/src/pages/Cart.tsx`
- Rewrite: `frontend/src/pages/CheckoutSuccess.tsx`
- Rewrite: `frontend/src/pages/CheckoutCancel.tsx`
- Create: `backend/app/routers/cart.py`
- Create: `backend/app/models.py` (add CartItem model)
- Create: `backend/app/schemas.py` (add CartItem schemas)
- Modify: `backend/app/main.py` (register cart router)

**Interfaces:**
- Produces: `CartContext` with `{ items, addItem(), removeItem(), updateQuantity(), clearCart(), total, itemCount }`
- Backend: `GET/POST/PUT/DELETE /api/cart`
- Consumes: `Product` type, `/api/checkout/session` endpoint

- [ ] **Step 1: Add CartItem model to backend**

```python
# Add to backend/app/models.py

class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship(back_populates="cart_items")
```

Add `cart_items` relationship to User model:

```python
# In User class, add:
cart_items: Mapped[list["CartItem"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan",
)
```

- [ ] **Step 2: Add CartItem schemas**

```python
# Add to backend/app/schemas.py

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=10)

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1, le=10)

class CartItemOut(BaseModel):
    id: int
    product_id: str
    quantity: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

- [ ] **Step 3: Create cart router**

```python
# backend/app/routers/cart.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import CartItem, User
from app.schemas import CartItemCreate, CartItemOut, CartItemUpdate
from app.product import get_product

router = APIRouter(
    prefix="/api/cart",
    tags=["Cart"],
)


@router.get("", response_model=list[CartItemOut])
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .order_by(CartItem.created_at.desc())
        .all()
    )


@router.post(
    "",
    response_model=CartItemOut,
    status_code=status.HTTP_201_CREATED,
)
def add_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = get_product(item_data.product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    existing = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == item_data.product_id,
        )
        .first()
    )

    if existing:
        existing.quantity = min(10, existing.quantity + item_data.quantity)
        db.commit()
        db.refresh(existing)
        return existing

    cart_item = CartItem(
        user_id=current_user.id,
        product_id=item_data.product_id,
        quantity=item_data.quantity,
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.put("/{product_id}", response_model=CartItemOut)
def update_cart_item(
    product_id: str,
    item_data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == product_id,
        )
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found.",
        )

    cart_item.quantity = item_data.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == product_id,
        )
        .first()
    )

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found.",
        )

    db.delete(cart_item)
    db.commit()
```

- [ ] **Step 4: Register cart router in main.py**

```python
# backend/app/main.py — add import and include

from app.routers import auth, cart, checkout, orders, products, webhook

# After other includes:
app.include_router(cart.router)
```

- [ ] **Step 5: Create CartContext**

```typescript
// frontend/src/contexts/CartContext.tsx

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

  // Load products for reference
  useEffect(() => {
    api.get<Product[]>("/api/products").then(setProducts).catch(console.error);
  }, []);

  // Load cart from API or localStorage
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

  // Sync to localStorage for guests
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
```

- [ ] **Step 6: Add CartProvider to main.tsx**

```typescript
// frontend/src/main.tsx

import { CartProvider } from "./contexts/CartContext";

// Wrap inside AuthProvider:
<AuthProvider>
  <CartProvider>
    <App />
  </CartProvider>
</AuthProvider>
```

- [ ] **Step 7: Update Navbar with cart count**

Update Navbar to use CartContext for the badge count and AuthContext for user state:

```typescript
// frontend/src/components/layout/Navbar.tsx

import { Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { useCart } from "../../contexts/CartContext";
import { useState, useRef, useEffect } from "react";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const { itemCount } = useCart();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <nav className="sticky top-0 z-50 bg-surface/80 backdrop-blur-md border-b border-black/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="text-xl font-bold text-text">
            DevDesk
          </Link>

          <div className="hidden md:flex items-center gap-8">
            <Link
              to="/products"
              className="text-text-muted hover:text-text transition-colors"
            >
              Products
            </Link>
          </div>

          <div className="flex items-center gap-4">
            <Link
              to="/cart"
              className="relative p-2 text-text-muted hover:text-text transition-colors"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
                />
              </svg>
              {itemCount > 0 && (
                <span className="absolute -top-1 -right-1 h-5 w-5 rounded-full bg-primary text-white text-xs flex items-center justify-center font-medium">
                  {itemCount}
                </span>
              )}
            </Link>

            {isAuthenticated ? (
              <div className="relative" ref={dropdownRef}>
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="h-8 w-8 rounded-full bg-primary text-white flex items-center justify-center text-sm font-medium"
                >
                  {user?.email.charAt(0).toUpperCase()}
                </button>

                {dropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-surface rounded-lg shadow-lg border border-black/5 py-1">
                    <Link
                      to="/account"
                      onClick={() => setDropdownOpen(false)}
                      className="block px-4 py-2 text-sm text-text hover:bg-black/5"
                    >
                      My Account
                    </Link>
                    <button
                      onClick={() => {
                        logout();
                        setDropdownOpen(false);
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-text hover:bg-black/5"
                    >
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link
                to="/login"
                className="text-sm font-medium text-text-muted hover:text-text transition-colors"
              >
                Sign In
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
```

- [ ] **Step 8: Create CartItem component**

```typescript
// frontend/src/components/CartItem.tsx

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
```

- [ ] **Step 9: Implement Cart page**

```typescript
// frontend/src/pages/Cart.tsx

import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../contexts/CartContext";
import { useAuth } from "../contexts/AuthContext";
import CartItem from "../components/CartItem";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";
import { api } from "../services/api";
import { useState } from "react";

export default function Cart() {
  const { items, total, itemCount, isLoading, clearCart } = useCart();
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
```

- [ ] **Step 10: Add cart-based checkout endpoint to backend**

```python
# Add to backend/app/routers/checkout.py

class CartCheckoutRequest(BaseModel):
    items: list[CheckoutRequest]

@router.post(
    "/cart",
    response_model=CheckoutResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cart_checkout_session(
    checkout_request: CartCheckoutRequest,
    settings: Settings = Depends(get_settings),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CheckoutResponse:
    if not settings.stripe_secret_key.startswith("sk_test_"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe test key is not configured correctly.",
        )

    line_items = []
    for item in checkout_request.items:
        product = get_product(item.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found.",
            )
        line_items.append({
            "price_data": {
                "currency": product.currency,
                "product_data": {
                    "name": product.name,
                    "description": product.description,
                },
                "unit_amount": product.price_cents,
            },
            "quantity": item.quantity,
        })

    stripe.api_key = settings.stripe_secret_key

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=(
                f"{settings.frontend_url}/checkout/success"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=f"{settings.frontend_url}/checkout/cancel",
            metadata={
                "user_id": str(current_user.id),
                "cart_checkout": "true",
            },
        )
    except stripe.StripeError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    if not session.url:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Stripe did not return a checkout URL.",
        )

    return CheckoutResponse(
        checkout_url=session.url,
        session_id=session.id,
    )
```

Add imports at top of checkout.py:

```python
from app.dependencies import get_current_user
from app.models import User
```

- [ ] **Step 11: Implement CheckoutSuccess page**

```typescript
// frontend/src/pages/CheckoutSuccess.tsx

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
```

- [ ] **Step 12: Implement CheckoutCancel page**

```typescript
// frontend/src/pages/CheckoutCancel.tsx

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
```

- [ ] **Step 13: Verify cart flow works**

Start both backend and frontend. Test:
1. Add items to cart (as guest — localStorage)
2. Navigate to cart page
3. Sign in
4. Add items (as user — API)
5. Proceed to checkout → Stripe test page

- [ ] **Step 14: Commit and merge**

```bash
git add backend/app/routers/cart.py backend/app/models.py backend/app/schemas.py backend/app/routers/checkout.py backend/main.py frontend/
git commit -m "add cart system with api, context, and checkout integration"

# Merge to main
git checkout main
git merge feature/cart-system
```

---

## Task 6: Account Pages + User-Scoped Orders
**Branch:** `feature/account-orders`

**Files:**
- Rewrite: `frontend/src/pages/Account.tsx`
- Create: `frontend/src/pages/OrderDetail.tsx`
- Create: `frontend/src/components/OrderCard.tsx`
- Create: `frontend/src/components/ui/Badge.tsx`
- Modify: `backend/app/routers/orders.py` (user-scoped)
- Modify: `backend/app/routers/webhook.py` (fix indentation bug)

**Interfaces:**
- Consumes: `useAuth()` for user info, `GET /api/orders`, `GET /api/orders/:id`
- Produces: Account page with order history, order detail page

- [ ] **Step 1: Fix orders router — user-scoped queries**

```python
# backend/app/routers/orders.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Order, User
from app.schemas import OrderOut

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"],
)


@router.get("", response_model=list[OrderOut])
def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id,
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    return order
```

- [ ] **Step 2: Fix webhook indentation bug**

```python
# backend/app/routers/webhook.py — fix the indentation of the if block

    if event.type == "checkout.session.completed":
        checkout_session = event.data.object
        metadata = checkout_session.metadata

        stripe_session_id = checkout_session.id
        product_id = metadata.product_id
        quantity = int(metadata.quantity)

        existing_order = (
            db.query(Order)
            .filter(Order.stripe_session_id == stripe_session_id)
            .first()
        )

        if existing_order:
            print("Order already exists:", stripe_session_id)
            return {
                "received": True,
                "message": "Order already processed",
            }

        customer_email = None

        if checkout_session.customer_details:
            customer_email = checkout_session.customer_details.email

        user_id = None
        if metadata.get("user_id"):
            user_id = int(metadata.user_id)

        new_order = Order(
            stripe_session_id=stripe_session_id,
            product_id=product_id,
            quantity=quantity,
            payment_status=checkout_session.payment_status,
            amount_total=checkout_session.amount_total,
            customer_email=customer_email,
            user_id=user_id,
        )

        try:
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
        except Exception:
            db.rollback()
            raise

        print("ORDER SAVED:", new_order.id)

    return {"received": True}
```

- [ ] **Step 3: Create Badge component**

```typescript
// frontend/src/components/ui/Badge.tsx

interface BadgeProps {
  status: string;
}

const statusStyles: Record<string, string> = {
  paid: "bg-success/10 text-success",
  complete: "bg-success/10 text-success",
  pending: "bg-warning/10 text-warning",
  failed: "bg-error/10 text-error",
  unpaid: "bg-error/10 text-error",
};

export default function Badge({ status }: BadgeProps) {
  const style = statusStyles[status.toLowerCase()] || "bg-black/5 text-text-muted";

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${style}`}
    >
      {status}
    </span>
  );
}
```

- [ ] **Step 4: Create OrderCard component**

```typescript
// frontend/src/components/OrderCard.tsx

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
```

- [ ] **Step 5: Implement Account page**

```typescript
// frontend/src/pages/Account.tsx

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
```

- [ ] **Step 6: Implement OrderDetail page**

```typescript
// frontend/src/pages/OrderDetail.tsx

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
```

- [ ] **Step 7: Verify account pages work**

Test flow:
1. Register a new account
2. Add items to cart, checkout via Stripe test mode
3. Visit `/account` — should see order in history
4. Click order — should see order detail

- [ ] **Step 8: Commit and merge**

```bash
git add backend/app/routers/orders.py backend/app/routers/webhook.py frontend/
git commit -m "add account pages, user-scoped orders, fix webhook bug"

# Merge to main
git checkout main
git merge feature/account-orders
```

---

## Task 7: Backend — Password Reset + Auth Enhancements
**Branch:** `feature/password-reset`

**Files:**
- Modify: `backend/app/models.py` (add PasswordReset model)
- Modify: `backend/app/schemas.py` (add reset schemas)
- Modify: `backend/app/routers/auth.py` (add forgot/reset endpoints)
- Modify: `backend/app/security.py` (add password validation)

**Interfaces:**
- Produces: `POST /api/auth/forgot-password`, `POST /api/auth/reset-password`
- Consumes: `User` model, `hash_password()`, `verify_password()`

- [ ] **Step 1: Add PasswordReset model**

```python
# Add to backend/app/models.py

class PasswordReset(Base):
    __tablename__ = "password_resets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    token: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    used: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship()
```

- [ ] **Step 2: Add password reset schemas**

```python
# Add to backend/app/schemas.py

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    token: str
    message: str

class ResetPasswordRequest(BaseModel):
    token: str
    password: str = Field(min_length=8, max_length=128)
```

- [ ] **Step 3: Add password validation to security.py**

```python
# Add to backend/app/security.py

import re

def validate_password_strength(password: str) -> str | None:
    """Return error message if password is weak, None if valid."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    return None
```

- [ ] **Step 4: Add forgot-password and reset-password endpoints**

```python
# Add to backend/app/routers/auth.py

import secrets
from datetime import datetime, timedelta, timezone

from app.models import PasswordReset
from app.schemas import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
)
from app.security import validate_password_strength


@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == request.email.lower())
        .first()
    )

    if user is None:
        return ForgotPasswordResponse(
            token="",
            message="If an account exists with this email, a reset link has been generated.",
        )

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    reset = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=expires_at,
    )
    db.add(reset)
    db.commit()

    return ForgotPasswordResponse(
        token=token,
        message="If an account exists with this email, a reset link has been generated.",
    )


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    error = validate_password_strength(request.password)
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    reset = (
        db.query(PasswordReset)
        .filter(
            PasswordReset.token == request.token,
            PasswordReset.used == False,
            PasswordReset.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )

    if not reset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token.",
        )

    user = db.get(User, reset.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found.",
        )

    user.hashed_password = hash_password(request.password)
    reset.used = True
    db.commit()

    return {"message": "Password reset successful."}
```

- [ ] **Step 5: Add password validation to registration**

Update the register endpoint in `auth.py`:

```python
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    error = validate_password_strength(user_data.password)
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    normalized_email = user_data.email.lower()
    # ... rest of existing code
```

- [ ] **Step 6: Test password reset flow**

```bash
# Test forgot-password
curl -X POST http://localhost:8000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Test reset-password with returned token
curl -X POST http://localhost:8000/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{"token": "RETURNED_TOKEN", "password": "NewPass123"}'
```

- [ ] **Step 7: Commit and merge**

```bash
git add backend/
git commit -m "add password reset flow and password strength validation"

# Merge to main
git checkout main
git merge feature/password-reset
```

---

## Task 8: Polish — Responsive, Loading States, Error Handling
**Branch:** `feature/polish`

**Files:**
- Modify: Various frontend files for responsive tweaks
- Modify: Various pages for error/loading states

**Interfaces:**
- No new interfaces — visual polish only

- [ ] **Step 1: Add mobile hamburger menu to Navbar**

Update Navbar with a mobile menu toggle:

```typescript
// Add state and mobile menu to Navbar.tsx
const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

// Add hamburger button (visible on mobile only):
<button
  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
  className="md:hidden p-2 text-text-muted"
>
  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    {mobileMenuOpen ? (
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    ) : (
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    )}
  </svg>
</button>

// Add mobile menu panel:
{mobileMenuOpen && (
  <div className="md:hidden border-t border-black/5 py-4">
    <Link to="/products" className="block py-2 text-text-muted hover:text-text">Products</Link>
    <Link to="/cart" className="block py-2 text-text-muted hover:text-text">Cart ({itemCount})</Link>
    {isAuthenticated ? (
      <>
        <Link to="/account" className="block py-2 text-text-muted hover:text-text">Account</Link>
        <button onClick={logout} className="block py-2 text-text-muted hover:text-text">Sign Out</button>
      </>
    ) : (
      <Link to="/login" className="block py-2 text-text-muted hover:text-text">Sign In</Link>
    )}
  </div>
)}
```

- [ ] **Step 2: Add loading states to all pages**

Ensure every page that fetches data shows `<Spinner />` while loading and proper error messages on failure. Review each page and add if missing.

- [ ] **Step 3: Add error boundary**

```typescript
// frontend/src/components/ErrorBoundary.tsx

import { Component, type ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[50vh] flex items-center justify-center px-4">
          <div className="text-center">
            <h1 className="text-2xl font-bold mb-2">Something went wrong</h1>
            <p className="text-text-muted mb-4">
              An unexpected error occurred. Please try refreshing the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="text-primary hover:text-primary-dark font-medium"
            >
              Refresh Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

Add to App.tsx wrapping the Routes.

- [ ] **Step 4: Test responsive design**

Test at breakpoints:
- Mobile: 375px (iPhone SE)
- Tablet: 768px (iPad)
- Desktop: 1280px (laptop)

Verify:
- Navbar collapses to hamburger on mobile
- Product grid: 1col → 2col → 4col
- Cart layout stacks on mobile
- Forms are properly sized on all screens

- [ ] **Step 5: Run TypeScript check**

```bash
cd frontend && npm run build
```

Fix any TypeScript errors.

- [ ] **Step 6: Run lint**

```bash
cd frontend && npm run lint
```

Fix any lint errors.

- [ ] **Step 7: Commit and merge**

```bash
git add frontend/
git commit -m "add responsive design, loading states, error boundary, and polish"

# Merge to main
git checkout main
git merge feature/polish
```

---

## Task 9: Final Integration Test

- [ ] **Step 1: Start backend**

```bash
cd backend
python -m uvicorn main:app --reload
```

- [ ] **Step 2: Start frontend**

```bash
cd frontend
npm run dev
```

- [ ] **Step 3: Full flow test**

1. Visit `/` — Landing page loads with hero and featured products
2. Click "Browse Products" — `/products` shows 8 products with images
3. Click a product — Detail page shows with image, description, quantity selector
4. Click "Add to Cart" — Cart count updates in navbar
5. Visit `/cart` — Cart shows items with quantities and subtotals
6. Click "Sign In to Checkout" — Redirects to `/login`
7. Click "Create one" — Register page with password strength meter
8. Register a new account — Redirects to `/account`
9. Visit `/cart` again — "Proceed to Checkout" button now active
10. Click checkout — Redirects to Stripe test page
11. Use Stripe test card `4242 4242 4242 4242` — Complete payment
12. Redirect to `/checkout/success` — Success message, cart cleared
13. Visit `/account` — Order appears in history
14. Click order — Order detail page shows
15. Test forgot password flow — Generate token, reset password
16. Logout and login with new password — Works

- [ ] **Step 4: Final commit**

```bash
git add -A
git commit -m "devdesk payment app complete - portfolio-ready e-commerce store"
```

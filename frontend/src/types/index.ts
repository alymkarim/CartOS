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

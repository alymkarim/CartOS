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

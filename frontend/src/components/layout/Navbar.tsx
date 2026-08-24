import { Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { useCart } from "../../contexts/CartContext";
import { useState, useRef, useEffect } from "react";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const { itemCount } = useCart();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
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

        {mobileMenuOpen && (
          <div className="md:hidden border-t border-black/5 py-4">
            <Link to="/products" className="block py-2 text-text-muted hover:text-text" onClick={() => setMobileMenuOpen(false)}>Products</Link>
            <Link to="/cart" className="block py-2 text-text-muted hover:text-text" onClick={() => setMobileMenuOpen(false)}>Cart ({itemCount})</Link>
            {isAuthenticated ? (
              <>
                <Link to="/account" className="block py-2 text-text-muted hover:text-text" onClick={() => setMobileMenuOpen(false)}>Account</Link>
                <button onClick={() => { logout(); setMobileMenuOpen(false); }} className="block py-2 text-text-muted hover:text-text">Sign Out</button>
              </>
            ) : (
              <Link to="/login" className="block py-2 text-text-muted hover:text-text" onClick={() => setMobileMenuOpen(false)}>Sign In</Link>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}

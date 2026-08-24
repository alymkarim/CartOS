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

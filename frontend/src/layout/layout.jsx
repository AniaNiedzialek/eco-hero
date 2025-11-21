import { Link, NavLink, useLocation } from "react-router-dom";
import { useAuth } from "../auth/authContext";

const navItems = [
  { to: "/", label: "Home", requireAuth: false },
  { to: "/dashboard", label: "Dashboard", requireAuth: true },
  { to: "/features/barcode", label: "Scan", requireAuth: true },
  { to: "/features/search", label: "Search", requireAuth: true },
  { to: "/features/local-rules", label: "Local rules", requireAuth: true },
  { to: "/features/history", label: "History & pickups", requireAuth: true },
];

export default function Layout({ children }) {
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();

  return (
    <div className="app-shell">
      <header className="app-header">
        <Link to="/" className="brand">
          <span className="brand-mark">♻️</span>
          <span>EcoHero</span>
        </Link>

        <nav className="nav">
          {navItems.map((item) => {
            if (item.requireAuth && !isAuthenticated) return null;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
                }
              >
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <div className="auth-area">
          {isAuthenticated ? (
            <>
              <span className="user-email">{user?.email}</span>
              <button className="btn ghost" onClick={logout}>
                Log out
              </button>
            </>
          ) : location.pathname !== "/login" ? (
            <Link to="/login" className="btn primary small">
              Login
            </Link>
          ) : null}
        </div>
      </header>

      <main className="app-main">{children}</main>
    </div>
  );
}
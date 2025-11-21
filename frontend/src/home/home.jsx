import { Link } from "react-router-dom";
import { useAuth } from "../auth/authContext";

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="page">
      <section className="hero">
        <h1 className="title">Make every toss the right one.</h1>
        <p className="subtitle">
          EcoHero helps you decide whether an item belongs in recycling,
          compost, or landfill — using barcodes, local rules, and your own
          recycling history.
        </p>

        <div className="hero-actions">
          {isAuthenticated ? (
            <Link to="/dashboard" className="btn primary">
              Open dashboard
            </Link>
          ) : (
            <Link to="/login" className="btn primary">
              Get started
            </Link>
          )}
        </div>

        <div className="hero-features">
          <div className="pill">📷 Barcode lookup</div>
          <div className="pill">📍 Zipcode-based rules</div>
          <div className="pill">🕒 Pickup reminders & history</div>
        </div>
      </section>
    </div>
  );
}
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/authContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email.trim()) return;
    login(email.trim());
    navigate("/dashboard");
  };

  return (
    <div className="page-centered">
      <div className="card auth-card">
        <h1 className="title">Sign in to EcoHero</h1>
        <p className="subtitle">
          This login is lightweight and just remembers you on this device.
        </p>

        <form onSubmit={handleSubmit} className="form">
          <label className="field">
            <span>Email</span>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <button type="submit" className="btn primary">
            Continue
          </button>
        </form>
      </div>
    </div>
  );
}

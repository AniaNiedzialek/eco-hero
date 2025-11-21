import { useEffect, useState } from "react";
import { api } from "../api/api";

export default function LocalRules() {
  const [zip, setZip] = useState("");
  const [rules, setRules] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("ecohero_zip");
    if (saved) setZip(saved);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!zip.trim()) return;

    setError("");
    setRules([]);
    setLoading(true);

    try {
      localStorage.setItem("ecohero_zip", zip.trim());

      // Backend assumption:
      // router = APIRouter(prefix="/rules"); then GET /by-zip/{zip}
      const data = await api.get(`/rules/by-zip/${encodeURIComponent(zip)}`);
      setRules(data.rules || data || []);
    } catch (err) {
      setError(err.message || "Could not load local rules.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 className="title">Local recycling rules</h1>
      <p className="subtitle">
        Recycling rules change by city. Enter your zipcode to see what’s
        actually accepted near you.
      </p>

      <form onSubmit={handleSubmit} className="form inline-form">
        <input
          type="text"
          inputMode="numeric"
          pattern="\d*"
          placeholder="Zipcode (e.g. 94720)"
          value={zip}
          onChange={(e) => setZip(e.target.value)}
        />
        <button type="submit" className="btn primary" disabled={loading}>
          {loading ? "Loading..." : "Show rules"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {rules.length > 0 && (
        <div className="card result-card">
          <h2>What your area accepts</h2>
          <ul className="list">
            {rules.map((r, idx) => (
              <li key={idx} className="list-row vertical">
                <div className="list-title">{r.category || r.name || "Rule"}</div>
                <div className="list-subtitle">
                  {r.description || r.text || JSON.stringify(r)}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
import { useState } from "react";
import { api } from "../api/api";
import DispositionTag from "../shared/dispositionTag";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [zip, setZip] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setError("");
    setResults([]);
    setLoading(true);

    try {
      // Backend : GET /api/scanner/search?query=paper%20cup&zip=94720
      // OR WE COULD WIRE IT TO get_recycling_resources or similar method
      const params = new URLSearchParams();
      params.set("query", query);
      if (zip.trim()) params.set("zip", zip.trim());

      const data = await api.get(`/scanner/search?${params.toString()}`);
      const items = Array.isArray(data) ? data : data.results || [];
      setResults(items);
    } catch (err) {
      setError(err.message || "Search failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 className="title">Manual item search</h1>
      <p className="subtitle">
        Search by name when you don’t have a barcode handy (e.g. “pizza box”).
        Your backend can map these to materials/categories.
      </p>

      <form onSubmit={handleSubmit} className="form inline-form">
        <input
          type="text"
          placeholder="pizza box, plastic fork, glass jar..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <input
          type="text"
          placeholder="Zip (optional)"
          value={zip}
          onChange={(e) => setZip(e.target.value)}
        />
        <button type="submit" className="btn primary" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {results.length > 0 && (
        <div className="card result-card">
          <ul className="list">
            {results.map((item, idx) => (
              <li key={item.id || idx} className="list-row">
                <div>
                  <div className="list-title">
                    {item.name || item.title || "Item"}
                  </div>
                  {item.description && (
                    <div className="list-subtitle">{item.description}</div>
                  )}
                  {item.category && (
                    <div className="list-subtitle">
                      Category: {item.category}
                    </div>
                  )}
                </div>
                <DispositionTag value={item.disposition || item.status} />
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

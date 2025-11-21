import { useState } from "react";
import { api } from "../api/api";
import DispositionTag from "../shared/dispositionTag";

export default function Barcode() {
  const [barcode, setBarcode] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!barcode.trim()) return;

    setError("");
    setResult(null);
    setLoading(true);

    try {
      // Backend assumption: routers/scanner.py with something like: 
      // @router.get("/scanner/barcode/{code}")
      const data = await api.get(`/scanner/barcode/${encodeURIComponent(barcode)}`);
      setResult(data);
    } catch (err) {
      setError(err.message || "Could not look up that barcode.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1 className="title">Barcode lookup</h1>
      <p className="subtitle">
        Enter a barcode from a package to see how to dispose of it.
      </p>

      <form onSubmit={handleSubmit} className="form inline-form">
        <input
          type="text"
          placeholder="e.g. 012345678905"
          value={barcode}
          onChange={(e) => setBarcode(e.target.value)}
        />
        <button type="submit" className="btn primary" disabled={loading}>
          {loading ? "Checking..." : "Check item"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="card result-card">
          <div className="result-header">
            <h2>{result.name || result.title || "Item"}</h2>
            <DispositionTag value={result.disposition || result.status} />
          </div>
          {result.brand && (
            <p className="muted">
              <strong>Brand:</strong> {result.brand}
            </p>
          )}
          {result.material && (
            <p className="muted">
              <strong>Material:</strong> {result.material}
            </p>
          )}
          {result.notes && <p>{result.notes}</p>}

          {/* Helpful to wire to actual JSON structure */}
          <pre className="json-preview">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

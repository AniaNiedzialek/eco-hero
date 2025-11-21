import { useState } from "react";
import { api, type Resource } from "../lib/api";

export default function ScannerPage() {
  const [zip, setZip] = useState("94066");
  const [file, setFile] = useState<File | null>(null);
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [resources, setResources] = useState<Resource[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onAnalyze() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.scanUpload(file, zip);
      setResources(data);
    } catch (e: any) {
      setResources(null);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function onLookup() {
    if (!code) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.scanBarcode(code, zip);
      setResources(data);
    } catch (e: any) {
      setResources(null);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="container py-8">
      <div className="card p-6">
        <h1 className="text-3xl font-bold">Barcode scanner</h1>

        <div className="mt-6 grid md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-slate-700">ZIP</label>
            <input
              value={zip}
              onChange={(e) => setZip(e.target.value)}
              className="mt-2 w-full rounded-xl border px-4 py-3"
              placeholder="ZIP"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">Upload photo</label>
            <div className="mt-2 flex items-center gap-3">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              />
              {file && <span className="text-slate-700">{file.name}</span>}
            </div>
          </div>
        </div>

        <div className="mt-4 flex items-center gap-4">
          <button className="btn px-6 py-3" onClick={onAnalyze} disabled={loading || !file}>
            {loading ? "Analyzing…" : "Upload & analyze"}
          </button>
        </div>

        <div className="mt-6 grid md:grid-cols-[1fr_auto] gap-4">
          <input
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full rounded-xl border px-4 py-3"
            placeholder="Or enter barcode number"
          />
          <button className="btn px-6 py-3" onClick={onLookup} disabled={loading || !code}>
            Lookup
          </button>
        </div>

        {error && <div className="mt-6 text-red-600">{error}</div>}

        {resources && (
          <div className="mt-8">
            <div className="font-semibold mb-2">Nearby programs:</div>
            {resources.length === 0 ? (
              <div className="text-slate-600">No programs found.</div>
            ) : (
              <ul className="space-y-2">
                {resources.map((r) => (
                  <li key={r.ref}>
                    <a className="underline text-eco-700" href={r.ref} target="_blank" rel="noreferrer">
                      {r.program}
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </section>
  );
}

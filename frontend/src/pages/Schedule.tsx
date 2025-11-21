import React from "react";
import { api } from "../lib/api";

export default function SchedulePage() {
  const [address, setAddress] = React.useState("");
  const [zip, setZip] = React.useState("");
  const [result, setResult] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const data = await api.schedule({ address, zip_code: zip });
    setResult(data);
    setLoading(false);
  }

  return (
    <section className="space-y-6">
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Pickup schedule</h2>
        <form onSubmit={onSubmit} className="grid sm:grid-cols-3 gap-3">
          <div><label className="label">Address</label><input className="input" value={address} onChange={e=>setAddress(e.target.value)} /></div>
          <div><label className="label">ZIP</label><input className="input" value={zip} onChange={e=>setZip(e.target.value)} /></div>
          <button className="btn self-end">{loading ? "Loading..." : "Get schedule"}</button>
        </form>
      </div>
      {result && <pre className="card p-6 overflow-auto">{JSON.stringify(result, null, 2)}</pre>}
    </section>
  );
}

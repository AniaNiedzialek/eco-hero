import React from "react";
import { api } from "../lib/api";

export default function BinsPage() {
  const [address, setAddress] = React.useState("");
  const [radius, setRadius] = React.useState(5);
  const [bins, setBins] = React.useState<any[]>([]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    const data = await api.binsNear(address, radius, 15);
    setBins(data?.results || data || []);
  }

  return (
    <section className="space-y-6">
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Find nearby bins</h2>
        <form onSubmit={onSubmit} className="grid sm:grid-cols-[2fr_1fr_auto] gap-3">
          <input className="input" placeholder="Enter an address" value={address} onChange={e=>setAddress(e.target.value)} />
          <input className="input" type="number" min={1} max={25} value={radius} onChange={e=>setRadius(parseInt(e.target.value||"5"))} />
          <button className="btn">Search</button>
        </form>
      </div>

      {bins.length > 0 && (
        <div className="card p-6">
          <ul className="divide-y">
            {bins.map((b, i) => (
              <li key={i} className="py-3">
                <div className="font-medium">{b.name || b.type || "Recycling Bin"}</div>
                <div className="text-sm text-slate-600">{b.address}</div>
                {b.distance && <div className="text-sm mt-1">{b.distance.toFixed?.(2)} mi</div>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

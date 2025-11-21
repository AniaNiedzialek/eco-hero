import React from "react";
import { api } from "../lib/api";

type Rule = { material: string; instructions: string };

function ExpandableCard({ title, content }: { title: string; content: string }) {
  const [open, setOpen] = React.useState(false);

  return (
    <div className="card p-4">
      <div
        className="font-semibold text-eco-600 uppercase tracking-wide cursor-pointer flex justify-between"
        onClick={() => setOpen(!open)}
      >
        {title}
        <span>{open ? "−" : "+"}</span>
      </div>
      {open && (
        <pre className="text-sm text-slate-700 bg-slate-50 rounded-lg p-3 overflow-auto max-h-60 whitespace-pre-wrap mt-2">
          {content}
        </pre>
      )}
    </div>
  );
}


export default function RulesPage() {
  const [zip, setZip] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [rules, setRules] = React.useState<Rule[] | null>(null);
  const [error, setError] = React.useState<string | null>(null);

 async function onSubmit(e: React.FormEvent) {
  e.preventDefault();
  setLoading(true);
  setError(null);
  setRules(null);

  try {
    const data = await api.rules(zip.trim());
    console.log("Backend response:", data);

    // Case 1: direct array
    if (Array.isArray(data)) {
      setRules(data);
    }
    // Case 2: backend wraps in { rules: [...] }
    else if (data.rules && Array.isArray(data.rules)) {
      setRules(data.rules);
    }
    // Case 3: backend returns a single object
    else if (typeof data === "object") {
    const flat: any[] = [];
    for (const [key, value] of Object.entries(data)) {
        flat.push({
        material: key,
        instructions:
            typeof value === "object"
            ? JSON.stringify(value, null, 2)
            : String(value),
        });
    }
    setRules(flat);
    }



    // Case 4: simple string or message
    else {
      setRules([{ material: "Info", instructions: String(data) }]);
    }
  } catch (err: any) {
    setError(err?.message || "Failed to fetch rules.");
  } finally {
    setLoading(false);
  }
}



  return (
    <section className="space-y-6">
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Recycling rules</h2>
        <form onSubmit={onSubmit} className="grid sm:grid-cols-[1fr_auto] gap-3">
          <div>
            <label className="label">ZIP code</label>
            <input className="input" value={zip} onChange={e => setZip(e.target.value)} placeholder="e.g., 95112" />
          </div>
          <button className="btn self-end" disabled={loading || !zip}>
            {loading ? "Checking..." : "Check rules"}
          </button>
        </form>
      </div>

      {error && <div className="card p-4 text-red-700 bg-red-50 border-red-200">{error}</div>}

      {rules && (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
            {rules.map((r, i) => (
            <ExpandableCard key={i} title={r.material} content={r.instructions} />
            ))}
        </div>
        )}



    </section>
  );
}

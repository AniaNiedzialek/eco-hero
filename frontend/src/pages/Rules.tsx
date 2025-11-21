import React from "react";
import { api } from "../lib/api";

type RuleDetail = {
  guidance: string;
  bin: string;
  notes?: string;
  provenance?: string[];
};

type BackendResponse = {
  zip: string;
  match_level: string;
  match_name: string;
  region: { state: string; city: string | null };
  summary: string;
  rules: Record<string, RuleDetail>;
};

function InfoCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="card p-4">
      <div className="text-xs uppercase tracking-wide text-eco-600 font-semibold mb-2">
        {label}
      </div>
      <div className="text-slate-800 font-medium">{value}</div>
    </div>
  );
}

// Format material name: remove underscores, capitalize words
const formatMaterial = (str: string) => {
  return str
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

function RuleCard({ 
  material, 
  rule, 
  isOpen, 
  onToggle 
}: { 
  material: string; 
  rule: RuleDetail;
  isOpen: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="card p-5 hover:shadow-md transition-shadow">
      <div
        className="font-semibold text-eco-700 text-base cursor-pointer flex justify-between items-center"
        onClick={onToggle}
      >
        <span>{formatMaterial(material)}</span>
        <span className="text-2xl text-eco-500">{isOpen ? "−" : "+"}</span>
      </div>
      {isOpen && (
        <div className="mt-4 space-y-4 text-sm border-t border-slate-200 pt-4">
          <div>
            <div className="font-semibold text-eco-600 mb-2 text-xs uppercase tracking-wide">Guidance</div>
            <div className="text-slate-700 leading-relaxed">{rule.guidance}</div>
          </div>
          <div>
            <div className="font-semibold text-eco-600 mb-2 text-xs uppercase tracking-wide">Bin</div>
            <div className="text-slate-800 bg-eco-50 px-3 py-2 rounded-md inline-block font-medium">
              {rule.bin}
            </div>
          </div>
          {rule.notes && (
            <div>
              <div className="font-semibold text-eco-600 mb-2 text-xs uppercase tracking-wide">Notes</div>
              <div className="text-slate-600 italic leading-relaxed">{rule.notes}</div>
            </div>
          )}
          {rule.provenance && rule.provenance.length > 0 && (
            <div>
              <div className="font-semibold text-eco-600 mb-2 text-xs uppercase tracking-wide">Source</div>
              <div className="text-slate-600 text-xs leading-relaxed">
                {rule.provenance.join(", ")}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}


export default function RulesPage() {
  const [zip, setZip] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [data, setData] = React.useState<BackendResponse | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [openCards, setOpenCards] = React.useState<Record<string, boolean>>({});

  const toggleCard = (material: string) => {
    setOpenCards(prev => ({
      ...prev,
      [material]: !prev[material]
    }));
  };

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setData(null);
    setOpenCards({}); // Reset open cards on new search

    try {
      const response = await api.rules(zip.trim());
      console.log("Backend response:", response);
      setData(response);
    } catch (err: any) {
      setError(err?.message || "Failed to fetch rules.");
    } finally {
      setLoading(false);
    }
  }



  return (
    <section className="max-w-5xl mx-auto space-y-6 px-4">
      <div className="card p-6">
        <h2 className="text-2xl font-semibold mb-4">Recycling rules</h2>
        <form onSubmit={onSubmit} className="grid sm:grid-cols-[1fr_auto] gap-3">
          <div>
            <label className="label">ZIP code</label>
            <input
              className="input"
              value={zip}
              onChange={(e) => setZip(e.target.value)}
              placeholder="e.g., 95112"
            />
          </div>
          <button className="btn self-end" disabled={loading || !zip}>
            {loading ? "Checking..." : "Check rules"}
          </button>
        </form>
      </div>

      {error && (
        <div className="card p-4 text-red-700 bg-red-50 border-red-200">
          {error}
        </div>
      )}

      {data && (
        <div className="space-y-6">
          {/* Overview Section */}
          <div className="grid grid-cols-2 gap-4">
            <InfoCard label="ZIP Code" value={data.zip} />
            <InfoCard
              label="Region"
              value={`${data.region.state}${
                data.region.city ? `, ${data.region.city}` : ""
              }`}
            />
          </div>

          {/* Summary */}
          {data.summary && (
            <div className="card p-5 bg-eco-50 border-eco-200">
              <div className="text-xs uppercase tracking-wide text-eco-600 font-semibold mb-3">
                Summary
              </div>
              <div className="text-slate-700 leading-relaxed">{data.summary}</div>
            </div>
          )}

          {/* Rules List */}
          {data.rules && Object.keys(data.rules).length > 0 && (
            <div>
              <h3 className="text-xl font-semibold mb-4 text-slate-800">
                Rules by Material
              </h3>
              <div className="space-y-3">
                {Object.entries(data.rules).map(([material, rule]) => (
                  <RuleCard 
                    key={material} 
                    material={material} 
                    rule={rule}
                    isOpen={!!openCards[material]}
                    onToggle={() => toggleCard(material)}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

import React from "react";
import { api } from "../lib/api";

type ScheduleItem = {
  date: string;
  type: string;
};

type ScheduleResponse = {
  address: string;
  schedule: ScheduleItem[] | string;
  city: string;
  state: string;
  message?: string;
};

function ScheduleCard({ item }: { item: ScheduleItem }) {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      weekday: 'short',
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="card p-4 flex justify-between items-center hover:shadow-md transition-shadow">
      <div>
        <div className="font-semibold text-slate-800">{formatDate(item.date)}</div>
        <div className="text-sm text-slate-600 mt-1">{item.type}</div>
      </div>
      <div className="text-eco-600">
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
    </div>
  );
}

export default function SchedulePage() {
  const [address, setAddress] = React.useState("");
  const [zip, setZip] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [result, setResult] = React.useState<ScheduleResponse | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [sendingEmail, setSendingEmail] = React.useState(false);
  const [emailSuccess, setEmailSuccess] = React.useState(false);
  const [showEmailForm, setShowEmailForm] = React.useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setEmailSuccess(false);
    setShowEmailForm(false);

    try {
      const data = await api.schedule({ address, zip_code: zip });
      setResult(data);
    } catch (err: any) {
      setError(err?.message || "Failed to fetch schedule.");
    } finally {
      setLoading(false);
    }
  }

  async function sendScheduleToEmail(e: React.FormEvent) {
    e.preventDefault();
    setSendingEmail(true);
    setError(null);
    setEmailSuccess(false);

    try {
      await api.notify({ email, address, zip_code: zip });
      setEmailSuccess(true);
      setShowEmailForm(false);
    } catch (err: any) {
      setError(err?.message || "Failed to send email.");
    } finally {
      setSendingEmail(false);
    }
  }

  return (
    <section className="max-w-5xl mx-auto space-y-6 px-4">
      <div className="card p-6">
        <h2 className="text-2xl font-semibold mb-4">Pickup schedule</h2>
        <form onSubmit={onSubmit} className="grid sm:grid-cols-3 gap-3">
          <div>
            <label className="label">Address</label>
            <input 
              className="input" 
              value={address} 
              onChange={(e) => setAddress(e.target.value)} 
              placeholder="200 E Santa Clara St"
            />
          </div>
          <div>
            <label className="label">ZIP</label>
            <input 
              className="input" 
              value={zip} 
              onChange={(e) => setZip(e.target.value)} 
              placeholder="95112"
            />
          </div>
          <button className="btn self-end" disabled={loading || !address || !zip}>
            {loading ? "Loading..." : "Get schedule"}
          </button>
        </form>
      </div>

      {error && (
        <div className="card p-4 text-red-700 bg-red-50 border-red-200">
          {error}
        </div>
      )}

      {emailSuccess && (
        <div className="card p-4 text-green-700 bg-green-50 border-green-200">
          ✓ Schedule sent to {email} successfully!
        </div>
      )}

      {result && (
        <div className="space-y-6">
          {/* Address Info */}
          <div className="card p-5 bg-eco-50 border-eco-200">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs uppercase tracking-wide text-eco-600 font-semibold mb-2">
                  Location
                </div>
                <div className="text-slate-800 font-medium">{result.address}</div>
                <div className="text-sm text-slate-600 mt-1">
                  {result.city}, {result.state}
                </div>
              </div>
              {typeof result.schedule !== 'string' && result.schedule && Array.isArray(result.schedule) && result.schedule.length > 0 && (
                <button 
                  onClick={() => setShowEmailForm(!showEmailForm)}
                  className="btn-secondary text-sm"
                >
                  📧 Email schedule
                </button>
              )}
            </div>

            {/* Email Form */}
            {showEmailForm && (
              <form onSubmit={sendScheduleToEmail} className="mt-4 pt-4 border-t border-eco-300">
                <div className="flex gap-3">
                  <input
                    type="email"
                    className="input flex-1"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                  <button 
                    type="submit" 
                    className="btn"
                    disabled={sendingEmail}
                  >
                    {sendingEmail ? "Sending..." : "Send"}
                  </button>
                  <button 
                    type="button" 
                    onClick={() => setShowEmailForm(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}
          </div>

          {/* Schedule */}
          {typeof result.schedule === 'string' ? (
            <div className="card p-6 bg-blue-50 border-blue-200">
              <div className="text-sm text-blue-800 mb-3">
                Schedule information is available online for this city.
              </div>
              <a 
                href={result.schedule} 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center text-eco-600 hover:text-eco-700 font-medium"
              >
                View collection calendar
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            </div>
          ) : result.schedule && Array.isArray(result.schedule) && result.schedule.length > 0 ? (
            <div>
              <h3 className="text-xl font-semibold mb-4 text-slate-800">
                Upcoming Pickups
              </h3>
              <div className="space-y-3">
                {result.schedule.map((item, index) => (
                  <ScheduleCard key={index} item={item} />
                ))}
              </div>
            </div>
          ) : (
            <div className="card p-6 text-center text-slate-600">
              {result.message || "No scheduled pickups found for this address."}
            </div>
          )}
        </div>
      )}
    </section>
  );
}

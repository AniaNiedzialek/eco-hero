import { useState, useEffect } from "react";
import { auth } from "../lib/firebase";
import { reportBin } from "../lib/firestore";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

export default function ReportPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const binId = searchParams.get("binId");
  const mode = binId ? "issue" : "new_bin";

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [location, setLocation] = useState<{ lat: number; lon: number } | null>(null);
  const [formData, setFormData] = useState({
    type: mode === "issue" ? "Missing" : "Recycling",
    description: ""
  });

  useEffect(() => {
    if (mode === "new_bin" && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lon: position.coords.longitude
          });
        },
        (error) => {
          console.error("Error getting location:", error);
        }
      );
    }
  }, [mode]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!auth.currentUser) return;
    if (mode === "new_bin" && !location) return;

    setLoading(true);
    try {
      await reportBin(auth.currentUser.uid, {
        latitude: location?.lat,
        longitude: location?.lon,
        type: formData.type,
        description: formData.description,
        reportType: mode,
        binId: binId || undefined
      });
      setSuccess(true);
      setTimeout(() => navigate('/bins'), 2000);
    } catch (error) {
      console.error("Error submitting report:", error);
    } finally {
      setLoading(false);
    }
  }

  if (!auth.currentUser) {
    return (
      <div className="container py-8 text-center">
        <h1 className="text-2xl font-bold mb-4">Please log in to report</h1>
        <Link to="/" className="btn px-6 py-3">Go Home</Link>
      </div>
    );
  }

  return (
    <section className="container py-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">
        {mode === "issue" ? "Report Issue with Bin" : "Add New Bin Location"}
      </h1>
      
      {success ? (
        <div className="bg-green-50 text-green-700 p-6 rounded-xl text-center">
          <h2 className="text-xl font-bold mb-2">Thank You!</h2>
          <p>Your report has been submitted for review.</p>
        </div>
      ) : (
        <div className="card p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {mode === "new_bin" && (
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Location</label>
                {location ? (
                  <div className="bg-gray-50 p-3 rounded-lg text-sm text-gray-600 flex items-center gap-2">
                    📍 {location.lat.toFixed(6)}, {location.lon.toFixed(6)}
                    <span className="text-xs text-green-600 ml-auto font-medium">Detected</span>
                  </div>
                ) : (
                  <div className="bg-yellow-50 p-3 rounded-lg text-sm text-yellow-700">
                    Detecting your location... Please allow location access.
                  </div>
                )}
              </div>
            )}

            {mode === "issue" && (
              <div className="bg-blue-50 p-3 rounded-lg text-sm text-blue-700 mb-4">
                Reporting issue for Bin ID: <strong>{binId}</strong>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                {mode === "issue" ? "Issue Type" : "Bin Type"}
              </label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="w-full rounded-xl border px-4 py-3"
              >
                {mode === "new_bin" ? (
                  <>
                    <option value="Recycling">Recycling (Blue)</option>
                    <option value="Compost">Compost (Green)</option>
                    <option value="Trash">Trash (Gray/Black)</option>
                    <option value="E-Waste">E-Waste Drop-off</option>
                    <option value="Hazardous">Hazardous Waste</option>
                    <option value="Textile">Textile/Clothing</option>
                  </>
                ) : (
                  <>
                    <option value="Missing">Bin is Missing</option>
                    <option value="Damaged">Bin is Damaged</option>
                    <option value="Full">Bin is Full / Overflowing</option>
                    <option value="Incorrect">Incorrect Information</option>
                    <option value="Other">Other Issue</option>
                  </>
                )}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Description / Notes</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full rounded-xl border px-4 py-3 h-32"
                placeholder={mode === "issue" ? "Describe the issue..." : "Describe the location..."}
                required
              />
            </div>

            <button 
              type="submit" 
              className="btn w-full py-3"
              disabled={loading || (mode === "new_bin" && !location)}
            >
              {loading ? "Submitting..." : "Submit Report"}
            </button>
          </form>
        </div>
      )}
    </section>
  );
}

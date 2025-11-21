import { useState } from "react";
import { api, type ScanResult } from "../lib/api";
import { saveScanHistory } from "../lib/firestore";
import { auth } from "../lib/firebase";
import { Link } from "react-router-dom";

export default function ScannerPage() {
  const [zip, setZip] = useState("94066");
  const [file, setFile] = useState<File | null>(null);
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleScanSuccess(data: ScanResult, type: 'barcode' | 'image', barcode?: string) {
    setResult(data);
    
    // Save to history if user is logged in
    if (auth.currentUser) {
      try {
        await saveScanHistory(auth.currentUser.uid, {
          productName: data.product_name,
          material: data.material,
          recyclable: data.recyclable,
          barcode: barcode,
          scanType: type
        });
      } catch (err) {
        console.error("Failed to save history:", err);
      }
    }
  }

  async function onAnalyze() {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await api.scanUpload(file, zip);
      await handleScanSuccess(data, 'image');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function onLookup() {
    if (!code) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await api.scanBarcode(code, zip);
      await handleScanSuccess(data, 'barcode', code);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="container py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Scanner & AI Identification</h1>
        {auth.currentUser && (
          <Link to="/history" className="btn-secondary px-4 py-2 text-sm">
            View History
          </Link>
        )}
      </div>

      <div className="card p-6">
        <div className="mt-6 grid md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-slate-700">ZIP Code</label>
            <input
              value={zip}
              onChange={(e) => setZip(e.target.value)}
              className="mt-2 w-full rounded-xl border px-4 py-3"
              placeholder="ZIP"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700">Upload Photo (Product or Barcode)</label>
            <div className="mt-2 flex items-center gap-3">
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-eco-50 file:text-eco-700 hover:file:bg-eco-100"
              />
            </div>
          </div>
        </div>

        <div className="mt-4 flex items-center gap-4">
          <button className="btn px-6 py-3" onClick={onAnalyze} disabled={loading || !file}>
            {loading ? "Analyzing..." : "Identify from Photo"}
          </button>
        </div>

        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center" aria-hidden="true">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center">
            <span className="bg-white px-2 text-sm text-gray-500">OR</span>
          </div>
        </div>

        <div className="grid md:grid-cols-[1fr_auto] gap-4">
          <input
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full rounded-xl border px-4 py-3"
            placeholder="Enter barcode number manually"
          />
          <button className="btn px-6 py-3" onClick={onLookup} disabled={loading || !code}>
            Lookup Barcode
          </button>
        </div>

        {error && <div className="mt-6 p-4 bg-red-50 text-red-700 rounded-xl">{error}</div>}

        {result && (
          <div className="mt-8 border rounded-xl overflow-hidden">
            <div className={`p-4 ${result.recyclable ? 'bg-green-100' : 'bg-gray-100'}`}>
              <h2 className="text-xl font-bold flex items-center gap-2">
                {result.recyclable ? '♻️ Recyclable' : '🗑️ Not Recyclable'}
                <span className="text-sm font-normal text-gray-600 ml-auto">
                  Source: {result.data_source || 'AI'}
                </span>
              </h2>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <div className="text-sm text-gray-500">Product</div>
                <div className="font-semibold text-lg">{result.product_name}</div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-gray-500">Material</div>
                  <div>{result.material}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Bin Type</div>
                  <div className="font-medium text-eco-700">{result.bin_type}</div>
                </div>
              </div>

              <div>
                <div className="text-sm text-gray-500">Guidance</div>
                <p className="text-gray-700">{result.recycling_guidance}</p>
              </div>

              {result.special_notes && (
                <div className="bg-yellow-50 p-3 rounded-lg text-sm text-yellow-800">
                  <strong>Note:</strong> {result.special_notes}
                </div>
              )}

              {result.places && result.places.length > 0 ? (
                <div className="mt-6 pt-6 border-t">
                  <h3 className="font-semibold text-lg mb-3">Nearby Recycling Locations</h3>
                  <div className="space-y-3">
                    {result.places.map((place, idx) => (
                      <div key={idx} className="bg-gray-50 p-3 rounded-lg border hover:border-eco-500 transition-colors">
                        <div className="font-medium text-eco-800">{place.name}</div>
                        <div className="text-sm text-gray-600 mt-1">{place.address}</div>
                        {place.rating && (
                          <div className="flex items-center gap-1 mt-1 text-xs text-amber-600">
                            <span>★ {place.rating}</span>
                            <span className="text-gray-400">({place.user_ratings_total})</span>
                          </div>
                        )}
                        <a 
                          href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(place.name + " " + place.address)}&query_place_id=${place.place_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-blue-600 hover:underline mt-2 inline-block"
                        >
                          View on Map →
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="mt-4 pt-4 border-t">
                  <div className="text-sm text-gray-500 mb-2">Need to find a drop-off location?</div>
                  <div className="grid grid-cols-2 gap-3">
                    <a 
                      href={`https://search.earth911.com/?what=${encodeURIComponent(result.material || result.product_name)}&where=${zip}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors"
                    >
                      <span>Earth911</span>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                    </a>
                    <a 
                      href={`https://www.google.com/maps/search/${encodeURIComponent((result.material || result.product_name) + " recycling")} near ${zip}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg text-sm font-medium transition-colors"
                    >
                      <span>Google Maps</span>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                    </a>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

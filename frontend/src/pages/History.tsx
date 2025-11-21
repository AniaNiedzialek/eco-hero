import { useEffect, useState } from "react";
import { auth } from "../lib/firebase";
import { getUserScanHistory, getUserStats, type ScanHistoryItem } from "../lib/firestore";
import { Link } from "react-router-dom";

export default function HistoryPage() {
  const [history, setHistory] = useState<(ScanHistoryItem & { id: string })[]>([]);
  const [stats, setStats] = useState<{ totalScans: number; recyclableCount: number; thisMonthCount: number } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(async (user) => {
      if (user) {
        try {
          const [historyData, statsData] = await Promise.all([
            getUserScanHistory(user.uid),
            getUserStats(user.uid)
          ]);
          setHistory(historyData as any);
          setStats(statsData);
        } catch (error) {
          console.error("Error fetching history:", error);
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    });

    return () => unsubscribe();
  }, []);

  if (loading) return <div className="container py-8">Loading...</div>;

  if (!auth.currentUser) {
    return (
      <div className="container py-8 text-center">
        <h1 className="text-2xl font-bold mb-4">Please log in to view your history</h1>
        <Link to="/" className="btn px-6 py-3">Go Home</Link>
      </div>
    );
  }

  return (
    <section className="container py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Your Recycling Impact</h1>
        <Link to="/scanner" className="btn-secondary px-4 py-2 text-sm">Scan New Item</Link>
      </div>

      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card p-6 bg-eco-50 border-eco-100">
            <div className="text-3xl font-bold text-eco-700">{stats.totalScans}</div>
            <div className="text-sm text-gray-600">Total Items Scanned</div>
          </div>
          <div className="card p-6 bg-blue-50 border-blue-100">
            <div className="text-3xl font-bold text-blue-700">{stats.recyclableCount}</div>
            <div className="text-sm text-gray-600">Recyclable Items Found</div>
          </div>
          <div className="card p-6 bg-purple-50 border-purple-100">
            <div className="text-3xl font-bold text-purple-700">{stats.thisMonthCount}</div>
            <div className="text-sm text-gray-600">Items This Month</div>
          </div>
        </div>
      )}

      <h2 className="text-xl font-bold mb-4">Recent Scans</h2>
      
      {history.length === 0 ? (
        <div className="text-gray-500 text-center py-8 bg-gray-50 rounded-xl">
          No scan history yet. Start scanning to track your impact!
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((item) => (
            <div key={item.id} className="card p-4 flex items-center gap-4">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center text-xl ${item.recyclable ? 'bg-green-100' : 'bg-gray-100'}`}>
                {item.recyclable ? '♻️' : '🗑️'}
              </div>
              <div className="flex-1">
                <div className="font-semibold">{item.productName}</div>
                <div className="text-sm text-gray-500">
                  {item.material} • {item.timestamp.toLocaleDateString()}
                </div>
              </div>
              <div className="text-xs px-2 py-1 bg-gray-100 rounded text-gray-600 uppercase">
                {item.scanType}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

import { useEffect, useState } from "react";
import { api } from "../api/api";
import DispositionTag from "../shared/dispositionTag";

export default function History() {
  const [items, setItems] = useState([]);
  const [errorHistory, setErrorHistory] = useState("");
  const [loadingHistory, setLoadingHistory] = useState(true);

  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [stateCode, setStateCode] = useState("");
  const [zip, setZip] = useState("");
  const [email, setEmail] = useState("");
  const [schedule, setSchedule] = useState(null);
  const [scheduleMsg, setScheduleMsg] = useState("");
  const [loadingSchedule, setLoadingSchedule] = useState(false);
  const [errorSchedule, setErrorSchedule] = useState("");

  // loading history from /api/bin/history
  useEffect(() => {
    const load = async () => {
      setErrorHistory("");
      setLoadingHistory(true);
      try {
        const data = await api.get("/bin/history");
        setItems(data || []);
      } catch (err) {
        setErrorHistory(err.message || "Could not load history.");
      } finally {
        setLoadingHistory(false);
      }
    };
    load();
  }, []);

  const handleScheduleSubmit = async (e) => {
    e.preventDefault();
    if (!address.trim() || !zip.trim() || !email.trim()) {
      return;
    }

    setErrorSchedule("");
    setSchedule(null);
    setScheduleMsg("");
    setLoadingSchedule(true);

    try {
      // Backend asummption:
      // router = APIRouter(prefix="/collection");
      // POST /schedule -> uses schedule_service & notification_service
      const payload = {
        address: address.trim(),
        city: city.trim(),
        state: stateCode.trim(),
        zip_code: zip.trim(),
        email: email.trim(),
      };
      const data = await api.post("/collection/schedule", payload);
      setSchedule(data.schedule || data);
      setScheduleMsg(
        "Schedule retrieved. If email notifications are enabled on the backend, you should also receive an email."
      );
    } catch (err) {
      setErrorSchedule(err.message || "Could not fetch schedule.");
    } finally {
      setLoadingSchedule(false);
    }
  };

  return (
    <div className="page">
      <h1 className="title">History & pickup schedule</h1>
      <p className="subtitle">
        Review your recent scans and set up collection schedule alerts based on
        your address.
      </p>

      {/* Pickup schedule section */}
      <div className="card">
        <h2>Collection schedule & alerts</h2>
        <p className="muted">
          Your backend’s <code>collection</code> router can use{" "}
          <code>schedule_service</code> and <code>notification_service</code> to
          email this info.
        </p>

        <form onSubmit={handleScheduleSubmit} className="form">
          <label className="field">
            <span>Address</span>
            <input
              type="text"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder="123 Green St"
              required
            />
          </label>
          <label className="field">
            <span>City</span>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              placeholder="Eco City"
            />
          </label>
          <label className="field">
            <span>State</span>
            <input
              type="text"
              value={stateCode}
              onChange={(e) => setStateCode(e.target.value)}
              placeholder="CA"
            />
          </label>
          <label className="field">
            <span>Zipcode</span>
            <input
              type="text"
              value={zip}
              onChange={(e) => setZip(e.target.value)}
              placeholder="94720"
              required
            />
          </label>
          <label className="field">
            <span>Email for alerts</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </label>

          {errorSchedule && <div className="error">{errorSchedule}</div>}
          {scheduleMsg && <p className="muted">{scheduleMsg}</p>}

          <button
            type="submit"
            className="btn primary"
            disabled={loadingSchedule}
          >
            {loadingSchedule ? "Checking..." : "Get schedule"}
          </button>
        </form>

        {schedule && (
          <pre className="json-preview">
            {JSON.stringify(schedule, null, 2)}
          </pre>
        )}
      </div>

      {/* History section */}
      <div className="card result-card">
        <h2>Recent scanned items</h2>

        {loadingHistory && <p>Loading history…</p>}
        {errorHistory && <div className="error">{errorHistory}</div>}

        {!loadingHistory && !errorHistory && items.length === 0 && (
          <p className="muted">No items yet — scan or search something first.</p>
        )}

        {!loadingHistory && !errorHistory && items.length > 0 && (
          <ul className="list">
            {items.map((item, idx) => (
              <li key={item.id || idx} className="list-row">
                <div>
                  <div className="list-title">{item.name || "Item"}</div>
                  <div className="list-subtitle">
                    {item.barcode && <>Barcode: {item.barcode} · </>}
                    {item.scanned_at || item.timestamp || "Recently"}
                  </div>
                </div>
                <DispositionTag value={item.disposition || item.status} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
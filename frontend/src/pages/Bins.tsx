import React from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import { Icon } from "leaflet";
import { api } from "../lib/api";
import "leaflet/dist/leaflet.css";

// Fix for default marker icons in Leaflet with Vite
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

// @ts-ignore
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
});

type Bin = {
  id: number;
  lat: number;
  lon: number;
  tags: Record<string, string>;
  distance_miles: number;
};

// Component to adjust map view when center changes
function MapViewController({ center }: { center: [number, number] }) {
  const map = useMap();
  React.useEffect(() => {
    map.setView(center, 13);
  }, [center, map]);
  return null;
}

export default function BinsPage() {
  const [address, setAddress] = React.useState("");
  const [radius, setRadius] = React.useState(5);
  const [bins, setBins] = React.useState<Bin[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [centerCoords, setCenterCoords] = React.useState<[number, number]>([37.3541, -121.9552]); // Default: Santa Clara

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await api.binsNear(address, radius, 15);
      
      // Handle both old format (array) and new format (object with center + bins)
      let binsList: Bin[] = [];
      let center: [number, number] | null = null;
      
      if (Array.isArray(data)) {
        // Old format - just array of bins
        binsList = data;
        if (binsList.length > 0) {
          center = [binsList[0].lat, binsList[0].lon];
        }
      } else if (data?.bins) {
        // New format - object with center and bins
        binsList = data.bins;
        if (data.center) {
          center = [data.center.lat, data.center.lon];
        }
      }
      
      setBins(binsList);
      if (center) {
        setCenterCoords(center);
      }
    } catch (err: any) {
      setError(err.message || "Failed to fetch bins");
      setBins([]);
    } finally {
      setLoading(false);
    }
  }

  // Custom icons
  const userIcon = new Icon({
    iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png",
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });

  const binIcon = new Icon({
    iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
  });

  return (
    <section className="space-y-6">
      <div className="card p-6">
        <h2 className="text-2xl font-semibold mb-4 text-slate-800">Find nearby bins</h2>
        <form onSubmit={onSubmit} className="grid sm:grid-cols-[2fr_1fr_auto] gap-3">
          <input
            className="input"
            placeholder="e.g., 150 Alviso St, Santa Clara, CA"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            required
          />
          <input
            className="input"
            type="number"
            min={1}
            max={25}
            value={radius}
            onChange={(e) => setRadius(parseInt(e.target.value || "5"))}
            placeholder="Radius (miles)"
          />
          <button className="btn" disabled={loading}>
            {loading ? "Searching..." : "Search"}
          </button>
        </form>
        {error && (
          <div className="mt-3 text-sm text-red-600 bg-red-50 p-3 rounded">
            {error}
          </div>
        )}
        <div className="mt-3 text-sm text-slate-500">
          💡 Enter a full address with street, city, and state for best results
        </div>
      </div>

      {bins.length > 0 && (
        <>
          {/* Map View */}
          <div className="card overflow-hidden">
            <div style={{ height: "500px", width: "100%" }}>
              <MapContainer
                center={centerCoords}
                zoom={13}
                style={{ height: "100%", width: "100%" }}
              >
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <MapViewController center={centerCoords} />
                
                {/* User location marker (center) */}
                <Marker position={centerCoords} icon={userIcon}>
                  <Popup>
                    <strong>Your Location</strong>
                    <br />
                    {address}
                  </Popup>
                </Marker>

                {/* Bin markers */}
                {bins.map((bin) => (
                  <Marker
                    key={bin.id}
                    position={[bin.lat, bin.lon]}
                    icon={binIcon}
                  >
                    <Popup>
                      <div className="text-sm">
                        <div className="font-semibold text-eco-700">
                          {bin.tags?.amenity || "Recycling Bin"}
                        </div>
                        {bin.tags?.name && (
                          <div className="text-slate-600">{bin.tags.name}</div>
                        )}
                        <div className="text-slate-500 mt-1">
                          {bin.distance_miles} miles away
                        </div>
                      </div>
                    </Popup>
                  </Marker>
                ))}
              </MapContainer>
            </div>
          </div>

          {/* List View */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold mb-4 text-slate-800">
              Found {bins.length} bin{bins.length !== 1 ? "s" : ""}
            </h3>
            <div className="space-y-3">
              {bins.map((bin, i) => (
                <div
                  key={bin.id || i}
                  className="p-4 border border-slate-200 rounded-lg hover:border-eco-400 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="font-medium text-slate-800">
                        {bin.tags?.name || bin.tags?.amenity || "Recycling Bin"}
                      </div>
                      {bin.tags?.description && (
                        <div className="text-sm text-slate-600 mt-1">
                          {bin.tags.description}
                        </div>
                      )}
                      <div className="text-sm text-slate-500 mt-2">
                        📍 {bin.lat.toFixed(5)}, {bin.lon.toFixed(5)}
                      </div>
                    </div>
                    <div className="text-right ml-4">
                      <div className="text-lg font-semibold text-eco-600">
                        {bin.distance_miles} mi
                      </div>
                      <div className="text-xs text-slate-500">away</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {!loading && bins.length === 0 && address && (
        <div className="card p-8 text-center text-slate-600">
          <p>No bins found in this area. Try increasing the search radius.</p>
        </div>
      )}
    </section>
  );
}

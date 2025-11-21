import { Link } from "react-router-dom";

const tiles = [
  {
    to: "/features/barcode",
    title: "Scan by barcode",
    emoji: "📷",
    description: "Check an item’s barcode to see if it’s Recycle, Compost, or Landfill.",
  },
  {
    to: "/features/search",
    title: "Manual search",
    emoji: "🔍",
    description: "Type an item name like “pizza box” or “plastic fork”.",
  },
  {
    to: "/features/local-rules",
    title: "Local rules",
    emoji: "📍",
    description: "Enter your zipcode to see location-specific recycling rules.",
  },
  {
    to: "/features/history",
    title: "History & pickups",
    emoji: "🕒",
    description: "Review your scanned items and manage pickup day alerts.",
  },
];

export default function Dashboard() {
  return (
    <div className="page">
      <h1 className="title">EcoHero dashboard</h1>
      <p className="subtitle">
        Use these tools to keep compostables and recyclables out of the landfill.
      </p>

      <div className="tile-grid">
        {tiles.map((tile) => (
          <Link key={tile.to} to={tile.to} className="card tile">
            <div className="tile-emoji">{tile.emoji}</div>
            <h2>{tile.title}</h2>
            <p>{tile.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
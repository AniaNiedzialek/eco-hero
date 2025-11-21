export default function DispositionTag({ value }) {
  const v = (value || "").toLowerCase();

  let label = "Unknown";
  let cls = "chip chip-unknown";

  if (v === "recycle" || v === "recycling") {
    label = "Recycle";
    cls = "chip chip-recycle";
  } else if (v === "compost") {
    label = "Compost";
    cls = "chip chip-compost";
  } else if (v === "landfill" || v === "trash") {
    label = "Landfill";
    cls = "chip chip-landfill";
  }

  return <span className={cls}>{label}</span>;
}

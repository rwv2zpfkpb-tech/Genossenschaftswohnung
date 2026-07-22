const SKELETON_COUNT = 8;

function SkeletonCard() {
  return (
    <div
      style={{
        background: "#FFFFFF",
        border: "1px solid #E6E3DC",
        borderRadius: "10px",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div className="skeleton-shimmer" style={{ aspectRatio: "16/10" }} />
      <div style={{ padding: "14px 14px 16px", display: "flex", flexDirection: "column", gap: "9px" }}>
        <div className="skeleton-shimmer" style={{ height: "16px", width: "70%", borderRadius: "4px" }} />
        <div className="skeleton-shimmer" style={{ height: "12px", width: "50%", borderRadius: "4px" }} />
        <div className="skeleton-shimmer" style={{ height: "17px", width: "40%", borderRadius: "4px", marginTop: "4px" }} />
      </div>
    </div>
  );
}

/**
 * Platzhalter-Raster waehrend `GET /listings` laedt, damit die Seite nicht
 * leer wirkt (z.B. beim Render-Cold-Start des Backends).
 */
export default function ListingGridSkeleton() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(272px, 1fr))", gap: "18px", alignContent: "start" }}>
      {Array.from({ length: SKELETON_COUNT }).map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}

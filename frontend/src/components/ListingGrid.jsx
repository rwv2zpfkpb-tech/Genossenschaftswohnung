import ListingCard from "./ListingCard.jsx";

/**
 * Rasteransicht der gefilterten Inserate mit Leerzustand.
 * @param {{listings: Array<object>, onSelect: (id: number) => void}} props
 */
export default function ListingGrid({ listings, onSelect }) {
  if (listings.length === 0) {
    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100%",
          color: "#918D84",
          gap: "8px",
          paddingTop: "60px",
        }}
      >
        <div style={{ fontFamily: "'Source Serif 4', serif", fontSize: "19px", color: "#514E48" }}>
          Keine Wohnungen gefunden
        </div>
        <div style={{ fontSize: "13.5px" }}>Passe die Filter an oder setze sie zurück.</div>
      </div>
    );
  }

  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(272px, 1fr))", gap: "18px", alignContent: "start" }}>
      {listings.map((listing) => (
        <ListingCard key={listing.id} listing={listing} onSelect={onSelect} />
      ))}
    </div>
  );
}

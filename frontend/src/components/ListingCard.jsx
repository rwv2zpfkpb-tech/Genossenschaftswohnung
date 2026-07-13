import { formatPrice, formatRelativeDate, isNewListing } from "../utils/format.js";

const PLACEHOLDER_BG =
  "repeating-linear-gradient(135deg, #ECE9E2, #ECE9E2 11px, #E1DED5 11px, #E1DED5 22px)";

/**
 * Eine Wohnungskarte in der Rasteransicht.
 * @param {{listing: object, onSelect: (id: number) => void}} props
 */
export default function ListingCard({ listing, onSelect }) {
  const thumb = listing.bild_urls?.[0];

  return (
    <div
      className="listing-card"
      onClick={() => onSelect(listing.id)}
      style={{
        background: "#FFFFFF",
        border: "1px solid #E6E3DC",
        borderRadius: "10px",
        overflow: "hidden",
        cursor: "pointer",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div style={{ position: "relative", aspectRatio: "16/10", background: thumb ? "#ECE9E2" : PLACEHOLDER_BG }}>
        {thumb && (
          <img
            src={thumb}
            alt={listing.adresse}
            loading="lazy"
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        )}
        {isNewListing(listing.first_seen) && (
          <div
            style={{
              position: "absolute",
              top: "10px",
              left: "10px",
              background: "#2F6F4F",
              color: "#FFFFFF",
              fontSize: "11px",
              fontWeight: 700,
              padding: "3px 8px",
              borderRadius: "5px",
              letterSpacing: "0.02em",
            }}
          >
            NEU
          </div>
        )}
        {listing.bild_urls?.length > 0 && (
          <div
            style={{
              position: "absolute",
              bottom: "9px",
              right: "10px",
              background: "rgba(28,28,26,0.55)",
              color: "#FFFFFF",
              fontSize: "10.5px",
              fontFamily: "monospace",
              padding: "2px 7px",
              borderRadius: "4px",
            }}
          >
            1/{listing.bild_urls.length}
          </div>
        )}
      </div>
      <div style={{ padding: "14px 14px 16px", display: "flex", flexDirection: "column", gap: "7px", flex: 1 }}>
        <div style={{ fontFamily: "'Source Serif 4', serif", fontSize: "16px", fontWeight: 600, lineHeight: 1.25 }}>
          {listing.adresse}
        </div>
        <div style={{ fontSize: "12.5px", color: "#6B6862" }}>
          {listing.viertel ?? "Viertel unbekannt"} · {listing.genossenschaft}
        </div>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginTop: "4px" }}>
          <div style={{ fontSize: "17px", fontWeight: 700 }}>{formatPrice(listing.preis)}</div>
          <div style={{ fontSize: "13px", color: "#514E48" }}>
            {listing.zimmer != null ? `${listing.zimmer} Zimmer` : "– Zimmer"}
            {listing.flaeche != null ? ` · ${listing.flaeche} m²` : ""}
          </div>
        </div>
        <div style={{ fontSize: "11.5px", color: "#918D84", marginTop: "2px" }}>
          {formatRelativeDate(listing.first_seen)}
        </div>
      </div>
    </div>
  );
}

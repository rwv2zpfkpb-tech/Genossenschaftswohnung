import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";

const ZURICH_CENTER = [47.3769, 8.5417];

/**
 * Kartenansicht mit einem Marker pro Inserat.
 * @param {{listings: Array<object>}} props
 */
export default function MapView({ listings }) {
  return (
    <MapContainer center={ZURICH_CENTER} zoom={12} style={{ height: "100%", width: "100%" }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {listings
        .filter((listing) => listing.lat != null && listing.lon != null)
        .map((listing) => (
          <Marker key={listing.id} position={[listing.lat, listing.lon]}>
            <Popup>
              <strong>{listing.adresse}</strong>
              <br />
              {listing.zimmer} Zimmer &middot; CHF {listing.preis}
              <br />
              <a href={listing.quelle_url} target="_blank" rel="noreferrer">
                Zum Inserat
              </a>
            </Popup>
          </Marker>
        ))}
    </MapContainer>
  );
}

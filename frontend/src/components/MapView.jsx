import { useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.markercluster";

import { formatPrice } from "../utils/format.js";

const ZURICH_CENTER = [47.3877, 8.5253];
const PLACEHOLDER_BG =
  "repeating-linear-gradient(135deg,#ECE9E2,#ECE9E2 9px,#E1DED5 9px,#E1DED5 18px)";

/**
 * Baut den Popup-Inhalt eines Markers per DOM-API statt HTML-Strings, damit
 * gescrapte Feldwerte (Adresse, Beschreibung, ...) nie als Markup landen.
 */
function buildPopupContent(listing, onSelect) {
  const container = document.createElement("div");

  const image = document.createElement("div");
  image.style.height = "100px";
  image.style.background = listing.bild_urls?.[0]
    ? `center / cover no-repeat url("${listing.bild_urls[0]}")`
    : PLACEHOLDER_BG;
  container.appendChild(image);

  const body = document.createElement("div");
  body.style.padding = "10px 12px";

  const title = document.createElement("div");
  title.style.fontFamily = "'Source Serif 4',serif";
  title.style.fontWeight = "600";
  title.style.fontSize = "14.5px";
  title.textContent = listing.adresse;
  body.appendChild(title);

  const subtitle = document.createElement("div");
  subtitle.style.fontSize = "12px";
  subtitle.style.color = "#6B6862";
  subtitle.style.marginTop = "2px";
  subtitle.textContent = `${listing.viertel ?? "Viertel unbekannt"} · ${listing.genossenschaft}`;
  body.appendChild(subtitle);

  const priceRow = document.createElement("div");
  priceRow.style.display = "flex";
  priceRow.style.justifyContent = "space-between";
  priceRow.style.marginTop = "8px";
  priceRow.style.fontSize = "13px";

  const price = document.createElement("span");
  price.style.fontWeight = "700";
  price.textContent = formatPrice(listing.preis);
  priceRow.appendChild(price);

  if (listing.zimmer != null) {
    const zimmer = document.createElement("span");
    zimmer.style.color = "#514E48";
    zimmer.textContent = `${listing.zimmer} Zi.`;
    priceRow.appendChild(zimmer);
  }
  body.appendChild(priceRow);

  const actions = document.createElement("div");
  actions.style.display = "flex";
  actions.style.gap = "8px";
  actions.style.marginTop = "10px";

  const detailsButton = document.createElement("button");
  detailsButton.className = "gw-map-popup-button";
  detailsButton.style.background = "#2F6F4F";
  detailsButton.style.color = "#fff";
  detailsButton.textContent = "Details";
  detailsButton.addEventListener("click", () => onSelect(listing.id));
  actions.appendChild(detailsButton);

  const originalLink = document.createElement("a");
  originalLink.className = "gw-map-popup-button";
  originalLink.style.background = "#F0EEE8";
  originalLink.style.color = "#1C1C1A";
  originalLink.href = listing.quelle_url;
  originalLink.target = "_blank";
  originalLink.rel = "noreferrer";
  originalLink.textContent = "Original";
  actions.appendChild(originalLink);

  body.appendChild(actions);
  container.appendChild(body);
  return container;
}

function ClusterLayer({ listings, onSelect }) {
  const map = useMap();
  const clusterGroupRef = useRef(null);

  useEffect(() => {
    const clusterGroup = L.markerClusterGroup({ maxClusterRadius: 46 });
    clusterGroupRef.current = clusterGroup;
    map.addLayer(clusterGroup);
    return () => {
      map.removeLayer(clusterGroup);
    };
  }, [map]);

  useEffect(() => {
    const clusterGroup = clusterGroupRef.current;
    if (!clusterGroup) return;
    clusterGroup.clearLayers();
    listings
      .filter((listing) => listing.lat != null && listing.lon != null)
      .forEach((listing) => {
        const icon = L.divIcon({
          className: "gw-price-pin",
          html:
            '<div style="background:#FFFFFF;border:1.5px solid #2F6F4F;color:#1C1C1A;font-family:\'IBM Plex Sans\',sans-serif;font-weight:700;font-size:11.5px;padding:4px 8px;border-radius:14px;white-space:nowrap;box-shadow:0 2px 6px rgba(28,28,26,0.18);">' +
            formatPrice(listing.preis) +
            "</div>",
          iconSize: null,
          iconAnchor: [30, 14],
        });
        const marker = L.marker([listing.lat, listing.lon], { icon });
        marker.bindPopup(() => buildPopupContent(listing, onSelect), { minWidth: 240 });
        clusterGroup.addLayer(marker);
      });
  }, [listings, onSelect]);

  return null;
}

function InvalidateOnVisible({ visible }) {
  const map = useMap();
  useEffect(() => {
    if (!visible) return;
    const timer = setTimeout(() => map.invalidateSize(), 80);
    return () => clearTimeout(timer);
  }, [visible, map]);
  return null;
}

/**
 * Kartenansicht mit geclusterten Preis-Markern und Detail-Popups.
 * @param {{listings: Array<object>, visible: boolean, onSelect: (id: number) => void}} props
 */
export default function MapView({ listings, visible, onSelect }) {
  return (
    <div style={{ position: "absolute", inset: 0, display: visible ? "block" : "none" }}>
      <MapContainer center={ZURICH_CENTER} zoom={12} style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          maxZoom={19}
        />
        <ClusterLayer listings={listings} onSelect={onSelect} />
        <InvalidateOnVisible visible={visible} />
      </MapContainer>
    </div>
  );
}

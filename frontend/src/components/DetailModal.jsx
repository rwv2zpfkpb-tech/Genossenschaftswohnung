import { useEffect, useState } from "react";

import { formatPrice, formatRelativeDate } from "../utils/format.js";

const PLACEHOLDER_BG =
  "repeating-linear-gradient(135deg, #ECE9E2, #ECE9E2 12px, #E1DED5 12px, #E1DED5 24px)";

/**
 * Detailansicht eines Inserats als modaler Dialog mit Bildergalerie.
 * @param {{listing: object, onClose: () => void}} props
 */
export default function DetailModal({ listing, onClose }) {
  const [galleryIndex, setGalleryIndex] = useState(0);
  const images = listing.bild_urls ?? [];

  useEffect(() => {
    setGalleryIndex(0);
  }, [listing.id]);

  useEffect(() => {
    const onKeyDown = (e) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(28,28,26,0.55)",
        zIndex: 1000,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "24px",
      }}
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "#FFFFFF",
          borderRadius: "14px",
          width: "100%",
          maxWidth: "680px",
          maxHeight: "88vh",
          overflowY: "auto",
          position: "relative",
          boxShadow: "0 20px 60px rgba(0,0,0,0.25)",
        }}
      >
        <button
          onClick={onClose}
          aria-label="Schliessen"
          style={{
            position: "absolute",
            top: "14px",
            right: "14px",
            zIndex: 10,
            width: "32px",
            height: "32px",
            borderRadius: "50%",
            border: "none",
            background: "rgba(28,28,26,0.65)",
            color: "#FFFFFF",
            fontSize: "16px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          ✕
        </button>

        <div
          style={{
            aspectRatio: "16/9",
            background: images[galleryIndex] ? "#ECE9E2" : PLACEHOLDER_BG,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
          }}
        >
          {images[galleryIndex] ? (
            <img
              src={images[galleryIndex]}
              alt={listing.adresse}
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          ) : (
            <div
              style={{
                fontFamily: "monospace",
                fontSize: "12px",
                color: "#918D84",
                background: "rgba(255,255,255,0.75)",
                padding: "4px 10px",
                borderRadius: "5px",
              }}
            >
              Keine Fotos vorhanden
            </div>
          )}
        </div>

        {images.length > 1 && (
          <div style={{ display: "flex", gap: "8px", padding: "12px 20px 0" }}>
            {images.map((url, i) => (
              <div
                key={url}
                onClick={() => setGalleryIndex(i)}
                style={{
                  width: "52px",
                  height: "38px",
                  borderRadius: "5px",
                  cursor: "pointer",
                  backgroundImage: `url(${url})`,
                  backgroundSize: "cover",
                  backgroundPosition: "center",
                  border: `2px solid ${i === galleryIndex ? "#2F6F4F" : "transparent"}`,
                }}
              />
            ))}
          </div>
        )}

        <div style={{ padding: "20px 24px 26px", display: "flex", flexDirection: "column", gap: "14px" }}>
          <div>
            <div style={{ fontFamily: "'Source Serif 4', serif", fontSize: "23px", fontWeight: 600, lineHeight: 1.25 }}>
              {listing.adresse}
            </div>
            <div style={{ fontSize: "13.5px", color: "#6B6862", marginTop: "3px" }}>
              {listing.viertel ?? "Viertel unbekannt"} · {listing.genossenschaft}
            </div>
          </div>

          <div style={{ display: "flex", gap: "28px", padding: "14px 0", borderTop: "1px solid #EEECE5", borderBottom: "1px solid #EEECE5", flexWrap: "wrap" }}>
            <div>
              <div style={{ fontSize: "11.5px", color: "#918D84" }}>Preis</div>
              <div style={{ fontSize: "17px", fontWeight: 700, marginTop: "2px" }}>{formatPrice(listing.preis)}</div>
            </div>
            <div>
              <div style={{ fontSize: "11.5px", color: "#918D84" }}>Zimmer</div>
              <div style={{ fontSize: "17px", fontWeight: 700, marginTop: "2px" }}>{listing.zimmer ?? "–"}</div>
            </div>
            <div>
              <div style={{ fontSize: "11.5px", color: "#918D84" }}>Fläche</div>
              <div style={{ fontSize: "17px", fontWeight: 700, marginTop: "2px" }}>
                {listing.flaeche != null ? `${listing.flaeche} m²` : "–"}
              </div>
            </div>
            <div>
              <div style={{ fontSize: "11.5px", color: "#918D84" }}>Erfasst</div>
              <div style={{ fontSize: "15px", fontWeight: 600, marginTop: "3px", color: "#514E48" }}>
                {formatRelativeDate(listing.first_seen)}
              </div>
            </div>
          </div>

          {listing.beschreibung && (
            <div style={{ fontSize: "14px", lineHeight: 1.6, color: "#33312C" }}>{listing.beschreibung}</div>
          )}

          <a
            href={listing.quelle_url}
            target="_blank"
            rel="noreferrer"
            style={{
              marginTop: "6px",
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "6px",
              background: "#2F6F4F",
              color: "#FFFFFF",
              textDecoration: "none",
              fontSize: "14px",
              fontWeight: 600,
              padding: "12px 18px",
              borderRadius: "8px",
            }}
          >
            Zum Original-Inserat →
          </a>
        </div>
      </div>
    </div>
  );
}

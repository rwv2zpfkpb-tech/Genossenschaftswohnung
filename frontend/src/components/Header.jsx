const toggleBaseStyle = {
  padding: "7px 16px",
  border: "none",
  borderRadius: "6px",
  fontSize: "13px",
  fontFamily: "'IBM Plex Sans',sans-serif",
  fontWeight: 600,
  cursor: "pointer",
};

const activeToggleStyle = {
  ...toggleBaseStyle,
  background: "#FFFFFF",
  color: "#1C1C1A",
  boxShadow: "0 1px 2px rgba(28,28,26,0.12)",
};

const inactiveToggleStyle = {
  ...toggleBaseStyle,
  background: "transparent",
  color: "#6B6862",
};

/**
 * Kopfzeile mit Titel und Liste/Karte-Umschalter.
 * @param {{view: "list" | "map", onViewChange: (view: "list" | "map") => void}} props
 */
export default function Header({ view, onViewChange }) {
  return (
    <div
      style={{
        flexShrink: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "16px",
        padding: "14px 24px",
        background: "#FFFFFF",
        borderBottom: "1px solid #E6E3DC",
        flexWrap: "wrap",
      }}
    >
      <div>
        <div
          style={{
            fontFamily: "'Source Serif 4', serif",
            fontSize: "21px",
            fontWeight: 600,
            letterSpacing: "-0.01em",
            lineHeight: 1.2,
          }}
        >
          Genossenschaftswohnungen Zürich
        </div>
        <div style={{ fontSize: "12.5px", color: "#6B6862", marginTop: "2px" }}>
          Aktuelle Inserate aller erfassten Baugenossenschaften
        </div>
      </div>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "2px",
          background: "#F0EEE8",
          borderRadius: "9px",
          padding: "3px",
          flexShrink: 0,
        }}
      >
        <button style={view === "list" ? activeToggleStyle : inactiveToggleStyle} onClick={() => onViewChange("list")}>
          Liste
        </button>
        <button style={view === "map" ? activeToggleStyle : inactiveToggleStyle} onClick={() => onViewChange("map")}>
          Karte
        </button>
      </div>
    </div>
  );
}

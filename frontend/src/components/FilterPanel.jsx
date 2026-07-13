import { useState } from "react";

/**
 * Filterleiste mit Preis-, Zimmer- und Groessen-Reglern sowie Viertel-Mehrfachauswahl.
 * @param {{
 *   priceMax: number, onPriceMaxChange: (v: number) => void,
 *   zimmerMin: number, onZimmerMinChange: (v: number) => void,
 *   qmMax: number, onQmMaxChange: (v: number) => void,
 *   viertelOptions: Array<{name: string, checked: boolean, count: number, toggle: () => void}>,
 *   resultCountText: string,
 *   onReset: () => void,
 * }} props
 */
export default function FilterPanel({
  priceMax,
  onPriceMaxChange,
  zimmerMin,
  onZimmerMinChange,
  qmMax,
  onQmMaxChange,
  viertelOptions,
  resultCountText,
  onReset,
}) {
  const [viertelOpen, setViertelOpen] = useState(false);
  const activeViertelCount = viertelOptions.filter((v) => v.checked).length;
  const viertelButtonLabel = activeViertelCount === 0 ? "Alle Viertel" : `${activeViertelCount} Viertel ausgewählt`;

  return (
    <div
      style={{
        flexShrink: 0,
        display: "flex",
        alignItems: "flex-end",
        gap: "28px",
        padding: "14px 24px",
        background: "#FFFFFF",
        borderBottom: "1px solid #E6E3DC",
        flexWrap: "wrap",
        rowGap: "16px",
      }}
    >
      <div style={{ minWidth: "190px" }}>
        <div style={{ fontSize: "12px", color: "#6B6862", marginBottom: "6px", display: "flex", justifyContent: "space-between" }}>
          <span>Preis bis</span>
          <span style={{ fontWeight: 600, color: "#1C1C1A" }}>CHF {priceMax}.–</span>
        </div>
        <input
          type="range"
          min={800}
          max={3000}
          step={50}
          value={priceMax}
          onChange={(e) => onPriceMaxChange(Number(e.target.value))}
          style={{ width: "190px", accentColor: "#2F6F4F", cursor: "pointer" }}
        />
      </div>

      <div style={{ minWidth: "170px" }}>
        <div style={{ fontSize: "12px", color: "#6B6862", marginBottom: "6px", display: "flex", justifyContent: "space-between" }}>
          <span>Zimmer ab</span>
          <span style={{ fontWeight: 600, color: "#1C1C1A" }}>{zimmerMin} Zi.</span>
        </div>
        <input
          type="range"
          min={1}
          max={6}
          step={0.5}
          value={zimmerMin}
          onChange={(e) => onZimmerMinChange(Number(e.target.value))}
          style={{ width: "170px", accentColor: "#2F6F4F", cursor: "pointer" }}
        />
      </div>

      <div style={{ minWidth: "170px" }}>
        <div style={{ fontSize: "12px", color: "#6B6862", marginBottom: "6px", display: "flex", justifyContent: "space-between" }}>
          <span>Wohnungsgrösse bis</span>
          <span style={{ fontWeight: 600, color: "#1C1C1A" }}>{qmMax} m²</span>
        </div>
        <input
          type="range"
          min={30}
          max={160}
          step={5}
          value={qmMax}
          onChange={(e) => onQmMaxChange(Number(e.target.value))}
          style={{ width: "170px", accentColor: "#2F6F4F", cursor: "pointer" }}
        />
      </div>

      <div style={{ position: "relative", minWidth: "170px" }}>
        <div style={{ fontSize: "12px", color: "#6B6862", marginBottom: "6px" }}>Viertel</div>
        <button
          onClick={() => setViertelOpen((open) => !open)}
          style={{
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "8px",
            padding: "8px 12px",
            background: "#FFFFFF",
            border: "1px solid #DAD7CF",
            borderRadius: "7px",
            fontSize: "13.5px",
            fontFamily: "'IBM Plex Sans',sans-serif",
            color: "#1C1C1A",
            cursor: "pointer",
          }}
        >
          <span>{viertelButtonLabel}</span>
          <span style={{ color: "#918D84", fontSize: "11px" }}>{viertelOpen ? "▲" : "▼"}</span>
        </button>
        {viertelOpen && (
          <>
            <div onClick={() => setViertelOpen(false)} style={{ position: "fixed", inset: 0, zIndex: 40 }} />
            <div
              style={{
                position: "absolute",
                top: "calc(100% + 6px)",
                left: 0,
                zIndex: 50,
                background: "#FFFFFF",
                border: "1px solid #E6E3DC",
                borderRadius: "9px",
                boxShadow: "0 8px 24px rgba(28,28,26,0.14)",
                padding: "8px",
                width: "230px",
                maxHeight: "280px",
                overflowY: "auto",
              }}
            >
              {viertelOptions.length === 0 && (
                <div style={{ padding: "7px 8px", fontSize: "13px", color: "#918D84" }}>Keine Viertel erfasst</div>
              )}
              {viertelOptions.map((v) => (
                <label
                  key={v.name}
                  className="viertel-option"
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "9px",
                    padding: "7px 8px",
                    borderRadius: "6px",
                    cursor: "pointer",
                    fontSize: "13.5px",
                  }}
                >
                  <input
                    type="checkbox"
                    checked={v.checked}
                    onChange={v.toggle}
                    style={{ accentColor: "#2F6F4F", width: "15px", height: "15px", cursor: "pointer" }}
                  />
                  <span style={{ flex: 1 }}>{v.name}</span>
                  <span style={{ color: "#918D84", fontSize: "12px" }}>{v.count}</span>
                </label>
              ))}
            </div>
          </>
        )}
      </div>

      <div style={{ flex: 1 }} />

      <div style={{ fontSize: "13.5px", color: "#1C1C1A", fontWeight: 600, paddingBottom: "9px", whiteSpace: "nowrap" }}>
        {resultCountText}
      </div>

      <button
        className="filter-reset-button"
        onClick={onReset}
        style={{
          padding: "8px 14px",
          background: "#FFFFFF",
          border: "1px solid #DAD7CF",
          borderRadius: "7px",
          fontSize: "13px",
          fontFamily: "'IBM Plex Sans',sans-serif",
          color: "#514E48",
          cursor: "pointer",
          marginBottom: 0,
        }}
      >
        Zurücksetzen
      </button>
    </div>
  );
}

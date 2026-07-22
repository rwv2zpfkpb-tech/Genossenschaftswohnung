import { useState } from "react";

/**
 * Zweiseitiger Range-Slider (Minimum- und Maximum-Griff) auf Basis zweier
 * ueberlagerter <input type="range">-Elemente.
 * @param {{
 *   min: number, max: number, step: number,
 *   valueMin: number, valueMax: number,
 *   onChange: (min: number, max: number) => void,
 *   width: string,
 * }} props
 */
function RangeSlider({ min, max, step, valueMin, valueMax, onChange, width }) {
  const percentMin = ((valueMin - min) / (max - min)) * 100;
  const percentMax = ((valueMax - min) / (max - min)) * 100;

  const handleMinChange = (e) => {
    const next = Math.min(Number(e.target.value), valueMax - step);
    onChange(next, valueMax);
  };

  const handleMaxChange = (e) => {
    const next = Math.max(Number(e.target.value), valueMin + step);
    onChange(valueMin, next);
  };

  return (
    <div style={{ position: "relative", height: "24px", width }}>
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: 0,
          right: 0,
          transform: "translateY(-50%)",
          height: "4px",
          borderRadius: "2px",
          background: "#E6E3DC",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: `${percentMin}%`,
          width: `${percentMax - percentMin}%`,
          transform: "translateY(-50%)",
          height: "4px",
          borderRadius: "2px",
          background: "#2F6F4F",
        }}
      />
      <input
        type="range"
        className="gw-range-input"
        min={min}
        max={max}
        step={step}
        value={valueMin}
        onChange={handleMinChange}
        style={{ zIndex: valueMin > (min + max) / 2 ? 5 : 3 }}
      />
      <input
        type="range"
        className="gw-range-input"
        min={min}
        max={max}
        step={step}
        value={valueMax}
        onChange={handleMaxChange}
        style={{ zIndex: 4 }}
      />
    </div>
  );
}

/**
 * Filterleiste mit Preis-, Zimmer- und Groessen-Reglern (jeweils als Min/Max-Range)
 * sowie Viertel-Mehrfachauswahl.
 * @param {{
 *   priceMin: number, priceMax: number, onPriceChange: (min: number, max: number) => void,
 *   zimmerMin: number, zimmerMax: number, onZimmerChange: (min: number, max: number) => void,
 *   qmMin: number, qmMax: number, onQmChange: (min: number, max: number) => void,
 *   viertelOptions: Array<{name: string, checked: boolean, count: number, toggle: () => void}>,
 *   resultCountText: string,
 *   onReset: () => void,
 * }} props
 */
export default function FilterPanel({
  priceMin,
  priceMax,
  onPriceChange,
  zimmerMin,
  zimmerMax,
  onZimmerChange,
  qmMin,
  qmMax,
  onQmChange,
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
          <span>Preis</span>
          <span style={{ fontWeight: 600, color: "#1C1C1A" }}>
            CHF {priceMin}.– – {priceMax}.–
          </span>
        </div>
        <RangeSlider
          min={800}
          max={3000}
          step={50}
          valueMin={priceMin}
          valueMax={priceMax}
          onChange={onPriceChange}
          width="190px"
        />
      </div>

      <div style={{ minWidth: "170px" }}>
        <div style={{ fontSize: "12px", color: "#6B6862", marginBottom: "6px", display: "flex", justifyContent: "space-between" }}>
          <span>Zimmer</span>
          <span style={{ fontWeight: 600, color: "#1C1C1A" }}>
            {zimmerMin} – {zimmerMax} Zi.
          </span>
        </div>
        <RangeSlider
          min={1}
          max={6}
          step={0.5}
          valueMin={zimmerMin}
          valueMax={zimmerMax}
          onChange={onZimmerChange}
          width="170px"
        />
      </div>

      <div style={{ minWidth: "170px" }}>
        <div style={{ fontSize: "12px", color: "#6B6862", marginBottom: "6px", display: "flex", justifyContent: "space-between" }}>
          <span>Wohnungsgrösse</span>
          <span style={{ fontWeight: 600, color: "#1C1C1A" }}>
            {qmMin} – {qmMax} m²
          </span>
        </div>
        <RangeSlider
          min={30}
          max={160}
          step={5}
          valueMin={qmMin}
          valueMax={qmMax}
          onChange={onQmChange}
          width="170px"
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

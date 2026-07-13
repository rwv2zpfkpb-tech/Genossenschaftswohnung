/**
 * Filterleiste fuer Zimmer, Quartier und Preis.
 * @param {{filters: object, onChange: (filters: object) => void}} props
 */
export default function FilterPanel({ filters, onChange }) {
  const handleChange = (key) => (event) => {
    onChange({ ...filters, [key]: event.target.value });
  };

  return (
    <div className="filter-panel">
      <label>
        Zimmer min.
        <input type="number" step="0.5" value={filters.roomsMin ?? ""} onChange={handleChange("roomsMin")} />
      </label>
      <label>
        Zimmer max.
        <input type="number" step="0.5" value={filters.roomsMax ?? ""} onChange={handleChange("roomsMax")} />
      </label>
      <label>
        Preis max. (CHF)
        <input type="number" value={filters.priceMax ?? ""} onChange={handleChange("priceMax")} />
      </label>
      <label>
        Quartier
        <input type="text" value={filters.quarter ?? ""} onChange={handleChange("quarter")} />
      </label>
    </div>
  );
}

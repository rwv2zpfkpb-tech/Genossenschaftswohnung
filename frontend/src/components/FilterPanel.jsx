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
        <input type="number" step="0.5" value={filters.zimmerMin ?? ""} onChange={handleChange("zimmerMin")} />
      </label>
      <label>
        Zimmer max.
        <input type="number" step="0.5" value={filters.zimmerMax ?? ""} onChange={handleChange("zimmerMax")} />
      </label>
      <label>
        Preis max. (CHF)
        <input type="number" value={filters.preisMax ?? ""} onChange={handleChange("preisMax")} />
      </label>
      <label>
        Viertel
        <input type="text" value={filters.viertel ?? ""} onChange={handleChange("viertel")} />
      </label>
    </div>
  );
}

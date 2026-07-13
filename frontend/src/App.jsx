import { useEffect, useMemo, useState } from "react";

import { fetchListings } from "./api/client.js";
import Header from "./components/Header.jsx";
import FilterPanel from "./components/FilterPanel.jsx";
import ListingGrid from "./components/ListingGrid.jsx";
import MapView from "./components/MapView.jsx";
import DetailModal from "./components/DetailModal.jsx";

const DEFAULT_PRICE_MAX = 3000;
const DEFAULT_ZIMMER_MIN = 1;
const DEFAULT_QM_MAX = 160;

export default function App() {
  const [listings, setListings] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const [view, setView] = useState("list");
  const [priceMax, setPriceMax] = useState(DEFAULT_PRICE_MAX);
  const [zimmerMin, setZimmerMin] = useState(DEFAULT_ZIMMER_MIN);
  const [qmMax, setQmMax] = useState(DEFAULT_QM_MAX);
  const [viertelSelected, setViertelSelected] = useState([]);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    fetchListings()
      .then(setListings)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filteredExclViertel = useMemo(
    () =>
      listings.filter((l) => {
        if (l.preis != null && l.preis > priceMax) return false;
        if (l.zimmer != null && l.zimmer < zimmerMin) return false;
        if (l.flaeche != null && l.flaeche > qmMax) return false;
        return true;
      }),
    [listings, priceMax, zimmerMin, qmMax],
  );

  const filtered = useMemo(
    () =>
      filteredExclViertel.filter(
        (l) => viertelSelected.length === 0 || viertelSelected.includes(l.viertel),
      ),
    [filteredExclViertel, viertelSelected],
  );

  const sortedListings = useMemo(
    () => [...filtered].sort((a, b) => new Date(b.first_seen) - new Date(a.first_seen)),
    [filtered],
  );

  const viertelOptions = useMemo(() => {
    const names = [...new Set(listings.map((l) => l.viertel).filter(Boolean))].sort((a, b) =>
      a.localeCompare(b, "de"),
    );
    return names.map((name) => ({
      name,
      checked: viertelSelected.includes(name),
      count: filteredExclViertel.filter((l) => l.viertel === name).length,
      toggle: () =>
        setViertelSelected((selected) =>
          selected.includes(name) ? selected.filter((v) => v !== name) : [...selected, name],
        ),
    }));
  }, [listings, filteredExclViertel, viertelSelected]);

  const selectedListing = selectedId != null ? listings.find((l) => l.id === selectedId) : null;

  const resetFilters = () => {
    setPriceMax(DEFAULT_PRICE_MAX);
    setZimmerMin(DEFAULT_ZIMMER_MIN);
    setQmMax(DEFAULT_QM_MAX);
    setViertelSelected([]);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        width: "100%",
        fontFamily: "'IBM Plex Sans', sans-serif",
        background: "#FAF9F6",
        color: "#1C1C1A",
        overflow: "hidden",
      }}
    >
      <Header view={view} onViewChange={setView} />

      <FilterPanel
        priceMax={priceMax}
        onPriceMaxChange={setPriceMax}
        zimmerMin={zimmerMin}
        onZimmerMinChange={setZimmerMin}
        qmMax={qmMax}
        onQmMaxChange={setQmMax}
        viertelOptions={viertelOptions}
        resultCountText={`${filtered.length} ${filtered.length === 1 ? "Wohnung gefunden" : "Wohnungen gefunden"}`}
        onReset={resetFilters}
      />

      <div style={{ flex: 1, position: "relative", overflow: "hidden" }}>
        {error && (
          <div style={{ padding: "22px 24px", color: "#B3352C", fontSize: "13.5px" }}>{error}</div>
        )}
        {!error && loading && (
          <div style={{ padding: "22px 24px", color: "#6B6862", fontSize: "13.5px" }}>Lade Inserate…</div>
        )}
        {!error && !loading && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              overflowY: "auto",
              padding: "22px 24px",
              display: view === "list" ? "block" : "none",
            }}
          >
            <ListingGrid listings={sortedListings} onSelect={setSelectedId} />
          </div>
        )}
        {!error && !loading && (
          <MapView listings={filtered} visible={view === "map"} onSelect={setSelectedId} />
        )}
      </div>

      {selectedListing && <DetailModal listing={selectedListing} onClose={() => setSelectedId(null)} />}
    </div>
  );
}

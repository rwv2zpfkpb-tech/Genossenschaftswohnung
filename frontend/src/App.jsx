import { useEffect, useState } from "react";

import { fetchListings } from "./api/client.js";
import FilterPanel from "./components/FilterPanel.jsx";
import MapView from "./components/MapView.jsx";

export default function App() {
  const [filters, setFilters] = useState({});
  const [listings, setListings] = useState([]);

  useEffect(() => {
    fetchListings(filters).then(setListings).catch(console.error);
  }, [filters]);

  return (
    <div className="app-layout" style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <FilterPanel filters={filters} onChange={setFilters} />
      <div style={{ flex: 1 }}>
        <MapView listings={listings} />
      </div>
    </div>
  );
}

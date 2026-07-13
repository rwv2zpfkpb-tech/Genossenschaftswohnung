const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

/**
 * Laedt Inserate vom Backend, gefiltert nach Zimmer, Preis und Viertel.
 * @param {{zimmerMin?: number, zimmerMax?: number, preisMax?: number, viertel?: string}} filters
 */
export async function fetchListings(filters = {}) {
  const params = new URLSearchParams();
  if (filters.zimmerMin != null) params.set("zimmer_min", filters.zimmerMin);
  if (filters.zimmerMax != null) params.set("zimmer_max", filters.zimmerMax);
  if (filters.preisMax != null) params.set("preis_max", filters.preisMax);
  if (filters.viertel) params.set("viertel", filters.viertel);

  const response = await fetch(`${API_BASE_URL}/listings?${params.toString()}`);
  if (!response.ok) {
    throw new Error(`Fehler beim Laden der Inserate: ${response.status}`);
  }
  return response.json();
}

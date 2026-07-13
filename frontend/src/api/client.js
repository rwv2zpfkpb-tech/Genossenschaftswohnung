const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

/**
 * Laedt Inserate vom Backend, gefiltert nach Zimmer, Preis und Quartier.
 * @param {{roomsMin?: number, roomsMax?: number, priceMax?: number, quarter?: string}} filters
 */
export async function fetchListings(filters = {}) {
  const params = new URLSearchParams();
  if (filters.roomsMin != null) params.set("rooms_min", filters.roomsMin);
  if (filters.roomsMax != null) params.set("rooms_max", filters.roomsMax);
  if (filters.priceMax != null) params.set("price_max", filters.priceMax);
  if (filters.quarter) params.set("quarter", filters.quarter);

  const response = await fetch(`${API_BASE_URL}/listings?${params.toString()}`);
  if (!response.ok) {
    throw new Error(`Fehler beim Laden der Inserate: ${response.status}`);
  }
  return response.json();
}

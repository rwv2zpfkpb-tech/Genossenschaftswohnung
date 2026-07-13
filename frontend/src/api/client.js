const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

/**
 * Laedt alle aktiven Inserate vom Backend. Preis-, Zimmer- und Viertel-Filter
 * werden im Frontend angewendet, damit die Quartier-Auswahl live Trefferzahlen
 * anzeigen kann, ohne bei jeder Filteraenderung neu zu laden.
 */
export async function fetchListings() {
  const response = await fetch(`${API_BASE_URL}/listings`);
  if (!response.ok) {
    throw new Error(`Fehler beim Laden der Inserate: ${response.status}`);
  }
  return response.json();
}

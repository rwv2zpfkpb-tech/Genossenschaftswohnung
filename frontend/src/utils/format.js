/**
 * Formatiert einen Preis in CHF mit Tausendertrennzeichen, z.B. "CHF 1'780.–".
 * @param {number | null | undefined} preis
 */
export function formatPrice(preis) {
  if (preis == null) return "Preis auf Anfrage";
  return "CHF " + String(preis).replace(/\B(?=(\d{3})+(?!\d))/g, "'") + ".–";
}

/**
 * Formatiert ein ISO-Datum als relative deutsche Zeitangabe, z.B. "vor 3 Tagen".
 * @param {string} iso
 */
export function formatRelativeDate(iso) {
  const days = Math.floor((Date.now() - new Date(iso).getTime()) / 86400000);
  if (days <= 0) return "heute inseriert";
  if (days === 1) return "gestern inseriert";
  if (days < 7) return `vor ${days} Tagen`;
  if (days < 14) return "vor 1 Woche";
  if (days < 30) return `vor ${Math.floor(days / 7)} Wochen`;
  const months = Math.floor(days / 30);
  return `vor ${months} ${months === 1 ? "Monat" : "Monaten"}`;
}

/**
 * Ob ein Inserat in den letzten 7 Tagen zum ersten Mal gesehen wurde.
 * @param {string} iso
 */
export function isNewListing(iso) {
  return (Date.now() - new Date(iso).getTime()) / 86400000 < 7;
}

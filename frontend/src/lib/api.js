// lib/api.js
export function buildMathUrl(ops, count, digits) {
  const baseUrl = import.meta.env.MODE === 'production' ? '' : 'http://localhost:8000';
  const query = ops.map(op => `operations=${op}`).join('&') + `&count=${count}&digits=${encodeURIComponent(digits)}`;
  return `${baseUrl}/api/math?${query}`; // <-- assure-toi qu'il n'y a PAS de /api ici
}

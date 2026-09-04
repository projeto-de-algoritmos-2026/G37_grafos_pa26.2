// Todas as chamadas passam por /api, que o Vite redireciona para a API em 8000.
const BASE = "/api";

export async function buscarStatusDoGrafo() {
  const resposta = await fetch(`${BASE}/status`);
  if (!resposta.ok) throw new Error("Nao foi possivel consultar o grafo");
  return resposta.json();
}

export async function calcularRota(origem, destino) {
  const resposta = await fetch(`${BASE}/rota`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      origem_lat: origem.lat,
      origem_lon: origem.lng,
      destino_lat: destino.lat,
      destino_lon: destino.lng,
    }),
  });

  if (resposta.status === 404) {
    const corpo = await resposta.json().catch(() => null);
    throw new Error(corpo?.detail ?? "Não existe caminho entre esses dois pontos.");
  }
  if (!resposta.ok) {
    throw new Error("A API respondeu com erro. O backend esta rodando?");
  }
  return resposta.json();
}

const API_URL = "http://127.0.0.1:8000";

// centro aproximado do Gama-DF
const mapa = L.map("mapa").setView([-16.0192, -48.0642], 14);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(mapa);

let marcadorOrigem = null;
let marcadorDestino = null;
let linhaRota = null;
let pontoOrigem = null;
let pontoDestino = null;

const instrucao = document.getElementById("instrucao");
const resultado = document.getElementById("resultado");

mapa.on("click", async (evento) => {
  const { lat, lng } = evento.latlng;

  if (!pontoOrigem) {
    pontoOrigem = { lat, lng };
    marcadorOrigem = L.marker([lat, lng], { title: "Origem" }).addTo(mapa);
    instrucao.textContent = "2. Clique no DESTINO";
    return;
  }

  if (!pontoDestino) {
    pontoDestino = { lat, lng };
    marcadorDestino = L.marker([lat, lng], { title: "Destino" }).addTo(mapa);
    instrucao.textContent = "Calculando rota...";
    await calcularRota();
  }
});

document.getElementById("limpar").addEventListener("click", () => {
  pontoOrigem = null;
  pontoDestino = null;
  if (marcadorOrigem) mapa.removeLayer(marcadorOrigem);
  if (marcadorDestino) mapa.removeLayer(marcadorDestino);
  if (linhaRota) mapa.removeLayer(linhaRota);
  instrucao.textContent = "1. Clique na ORIGEM";
  resultado.textContent = "";
});

async function calcularRota() {
  const corpo = {
    origem_lat: pontoOrigem.lat,
    origem_lon: pontoOrigem.lng,
    destino_lat: pontoDestino.lat,
    destino_lon: pontoDestino.lng,
  };

  try {
    const resposta = await fetch(`${API_URL}/rota`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(corpo),
    });

    if (!resposta.ok) {
      throw new Error("Nao foi possivel calcular a rota");
    }

    const dados = await resposta.json();

    if (linhaRota) mapa.removeLayer(linhaRota);

    linhaRota = L.polyline(dados.caminho_coordenadas, { color: "blue", weight: 5 }).addTo(mapa);
    mapa.fitBounds(linhaRota.getBounds());

    const minutos = (dados.tempo_estimado_segundos / 60).toFixed(1);
    resultado.innerHTML = `
      <b>Tempo estimado:</b> ${minutos} min<br/>
      <b>Nos visitados:</b> ${dados.nos_visitados}<br/>
      <b>Tempo de calculo:</b> ${dados.tempo_calculo_ms.toFixed(2)} ms
    `;
    instrucao.textContent = "Rota calculada! Clique em limpar para tentar outra.";
  } catch (erro) {
    resultado.textContent = "Erro: " + erro.message;
    instrucao.textContent = "Tente novamente.";
  }
}
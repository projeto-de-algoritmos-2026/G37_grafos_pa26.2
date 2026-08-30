import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dijkstra import dijkstra
from graph_loader import baixar_grafo_osm, no_mais_proximo

app = FastAPI(title="Rota Mais Rapida - Gama DF")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

grafo = None


@app.on_event("startup")
def carregar_grafo():
    global grafo
    grafo = baixar_grafo_osm()


class PedidoRota(BaseModel):
    origem_lat: float
    origem_lon: float
    destino_lat: float
    destino_lon: float


class RespostaRota(BaseModel):
    caminho_coordenadas: list[tuple[float, float]]
    tempo_estimado_segundos: float
    nos_visitados: int
    tempo_calculo_ms: float


@app.post("/rota", response_model=RespostaRota)
def calcular_rota(pedido: PedidoRota):
    no_origem = no_mais_proximo(grafo, pedido.origem_lat, pedido.origem_lon)
    no_destino = no_mais_proximo(grafo, pedido.destino_lat, pedido.destino_lon)

    inicio = time.perf_counter()
    caminho, custo, visitados = dijkstra(grafo, no_origem, no_destino)
    tempo_calculo_ms = (time.perf_counter() - inicio) * 1000

    if caminho is None:
        raise HTTPException(status_code=404, detail="Nao foi possivel encontrar uma rota entre os pontos.")

    coordenadas = [grafo.coordenadas[no_id] for no_id in caminho]

    return RespostaRota(
        caminho_coordenadas=coordenadas,
        tempo_estimado_segundos=custo,
        nos_visitados=visitados,
        tempo_calculo_ms=tempo_calculo_ms,
    )


@app.get("/status")
def status():
    return {
        "nos": grafo.numero_de_nos() if grafo else 0,
        "arestas": grafo.numero_de_arestas() if grafo else 0,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
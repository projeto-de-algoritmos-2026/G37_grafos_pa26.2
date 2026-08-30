import os
import pickle
import osmnx as ox
from graph import Grafo, distancia_haversine

CACHE_PATH = os.path.join(os.path.dirname(__file__), "gama_cache.pkl")

LOCAL_PADRAO = "Gama, Brasília, Brazil"


def _velocidade_padrao_kmh(dados_aresta: dict) -> float:
    maxspeed = dados_aresta.get("maxspeed")

    if isinstance(maxspeed, list):
        maxspeed = maxspeed[0]

    if maxspeed is None:
        return 40.0

    try:
        return float(str(maxspeed).split()[0])
    except (ValueError, IndexError):
        return 40.0


def baixar_grafo_osm(local: str = LOCAL_PADRAO, usar_cache: bool = True) -> Grafo:
    if usar_cache and os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)

    print(f"Baixando malha viaria de: {local} (pode demorar um pouco)...")
    grafo_osm = ox.graph_from_place(local, network_type="drive")

    grafo = Grafo()

    for no_id, dados in grafo_osm.nodes(data=True):
        grafo.adicionar_no(no_id, lat=dados["y"], lon=dados["x"])

    for origem, destino, dados in grafo_osm.edges(data=True):
        comprimento_m = dados.get("length", 0.0)
        velocidade_kmh = _velocidade_padrao_kmh(dados)
        velocidade_ms = velocidade_kmh * 1000 / 3600

        if velocidade_ms <= 0:
            continue

        tempo_segundos = comprimento_m / velocidade_ms
        grafo.adicionar_aresta(origem, destino, tempo_segundos)

    with open(CACHE_PATH, "wb") as f:
        pickle.dump(grafo, f)

    print(
        f"Grafo carregado: {grafo.numero_de_nos()} nos, "
        f"{grafo.numero_de_arestas()} arestas."
    )
    return grafo


def no_mais_proximo(grafo: Grafo, lat: float, lon: float) -> int:
    no_mais_perto = None
    menor_distancia = float("inf")

    for no_id, coord in grafo.coordenadas.items():
        distancia = distancia_haversine(coord, (lat, lon))
        if distancia < menor_distancia:
            menor_distancia = distancia
            no_mais_perto = no_id

    return no_mais_perto


if __name__ == "__main__":
    grafo = baixar_grafo_osm()
    print("Exemplo de no:", next(iter(grafo.adjacencia.items())))
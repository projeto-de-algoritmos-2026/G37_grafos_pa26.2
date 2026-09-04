import os
import pickle
import re

import osmnx as ox
from graph import Grafo

DIR_CACHE = os.path.join(os.path.dirname(__file__), "grafos")

# Cobre todo o Distrito Federal: Plano Piloto, Gama, Taguatinga, Ceilandia,
# Sobradinho e as demais regioes administrativas. Da para apontar para uma
# regiao menor (util em demonstracoes) com a variavel de ambiente REGIAO_OSM,
# por exemplo: REGIAO_OSM="Gama, Brasilia, Brazil" python main.py
LOCAL_PADRAO = os.environ.get("REGIAO_OSM", "Distrito Federal, Brazil")


def _caminho_cache(local: str) -> str:
    # Um arquivo por regiao: trocar de regiao nao invalida o cache da anterior.
    apelido = re.sub(r"[^a-z0-9]+", "-", local.lower()).strip("-")
    return os.path.join(DIR_CACHE, f"grafo-{apelido}.pkl")


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
    caminho_cache = _caminho_cache(local)

    if usar_cache and os.path.exists(caminho_cache):
        print(f"Carregando grafo de {local} do cache...")
        with open(caminho_cache, "rb") as f:
            grafo = pickle.load(f)
        print(
            f"Grafo carregado: {grafo.numero_de_nos()} nos, "
            f"{grafo.numero_de_arestas()} arestas."
        )
        return grafo

    print(f"Baixando malha viaria de: {local}")
    print("Na primeira execucao isso leva alguns minutos. Depois fica em cache.")
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

    os.makedirs(DIR_CACHE, exist_ok=True)
    with open(caminho_cache, "wb") as f:
        pickle.dump(grafo, f)

    print(
        f"Grafo carregado: {grafo.numero_de_nos()} nos, "
        f"{grafo.numero_de_arestas()} arestas."
    )
    return grafo


if __name__ == "__main__":
    grafo = baixar_grafo_osm()
    print("Exemplo de no:", next(iter(grafo.adjacencia.items())))

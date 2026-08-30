import heapq
from typing import Dict, List, Optional, Tuple
from graph import Grafo


def dijkstra(
    grafo: Grafo, origem: int, destino: int
) -> Tuple[Optional[List[int]], float, int]:
    
    distancia: Dict[int, float] = {origem: 0.0}
    anterior: Dict[int, int] = {}
    visitados = set()

    fila: List[Tuple[float, int]] = [(0.0, origem)]

    while fila:
        dist_atual, no_atual = heapq.heappop(fila)

        if no_atual in visitados:
            continue
        visitados.add(no_atual)

        if no_atual == destino:
            break

        for vizinho, peso in grafo.vizinhos(no_atual):
            nova_dist = dist_atual + peso
            if nova_dist < distancia.get(vizinho, float("inf")):
                distancia[vizinho] = nova_dist
                anterior[vizinho] = no_atual
                heapq.heappush(fila, (nova_dist, vizinho))

    if destino not in distancia:
        return None, float("inf"), len(visitados)

    caminho = [destino]
    atual = destino
    while atual != origem:
        atual = anterior[atual]
        caminho.append(atual)
    caminho.reverse()

    return caminho, distancia[destino], len(visitados)


if __name__ == "__main__":
    g = Grafo()
    for no, lat, lon in [("A", 0, 0), ("B", 0, 1), ("C", 0, 2), ("D", 0, 3)]:
        g.adicionar_no(no, lat, lon)
    g.adicionar_aresta("A", "B", 4)
    g.adicionar_aresta("A", "C", 1)
    g.adicionar_aresta("C", "B", 2)
    g.adicionar_aresta("B", "D", 1)
    g.adicionar_aresta("C", "D", 5)

    caminho, custo, visitados = dijkstra(g, "A", "D")
    print(f"Caminho: {caminho}, custo: {custo}, nos visitados: {visitados}")

import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


def distancia_haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    raio_terra = 6371000  # metros
 
    lat1_rad, lat2_rad = math.radians(lat1), math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
 
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return raio_terra * c


@dataclass
class Grafo: 
    adjacencia: Dict[int, List[Tuple[int, float]]] = field(default_factory=dict)
    coordenadas: Dict[int, Tuple[float, float]] = field(default_factory=dict)

    def adicionar_no(self, no_id: int, lat: float, lon: float) -> None:
        if no_id not in self.adjacencia:
            self.adjacencia[no_id] = []
        self.coordenadas[no_id] = (lat, lon)

    def adicionar_aresta(self, origem: int, destino: int, peso: float) -> None:
        if origem not in self.adjacencia:
            self.adjacencia[origem] = []
        self.adjacencia[origem].append((destino, peso))

    def vizinhos(self, no_id: int) -> List[Tuple[int, float]]:
        return self.adjacencia.get(no_id, [])

    def numero_de_nos(self) -> int:
        return len(self.adjacencia)

    def numero_de_arestas(self) -> int:
        return sum(len(v) for v in self.adjacencia.values())
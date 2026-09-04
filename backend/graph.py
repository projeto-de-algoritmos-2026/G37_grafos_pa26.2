import math
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, Tuple

METROS_POR_GRAU = 111_320  # aproximacao suficiente para comparar distancias


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


class IndiceEspacial:
    """Grade uniforme sobre as coordenadas dos nos.

    Sem ela, achar o no mais proximo de um clique exige comparar o ponto com
    todos os nos do grafo. No Distrito Federal inteiro (85 mil nos) isso custa
    ~67 ms por consulta, mais caro que o proprio Dijkstra. A grade divide o mapa
    em celulas e a busca visita apenas os aneis de celulas ao redor do clique,
    parando assim que o melhor candidato ja for mais perto do que qualquer no
    dos aneis seguintes.
    """

    LADO_CELULA_GRAUS = 0.01  # ~1,1 km
    LIMITE_ANEIS = 20  # alem disso o ponto esta longe da malha; varremos direto

    def __init__(self, coordenadas: Dict[int, Tuple[float, float]]) -> None:
        self.coordenadas = coordenadas
        self.celulas: Dict[Tuple[int, int], List[int]] = {}

        for no_id, (lat, lon) in coordenadas.items():
            self.celulas.setdefault(self._celula(lat, lon), []).append(no_id)

    def _celula(self, lat: float, lon: float) -> Tuple[int, int]:
        lado = self.LADO_CELULA_GRAUS
        return (math.floor(lat / lado), math.floor(lon / lado))

    def _nos_do_anel(self, linha: int, coluna: int, anel: int) -> Iterator[int]:
        if anel == 0:
            yield from self.celulas.get((linha, coluna), ())
            return

        for delta_linha in range(-anel, anel + 1):
            for delta_coluna in range(-anel, anel + 1):
                # so as celulas da borda do quadrado; o miolo ja foi visitado
                if max(abs(delta_linha), abs(delta_coluna)) != anel:
                    continue
                yield from self.celulas.get((linha + delta_linha, coluna + delta_coluna), ())

    def buscar(self, lat: float, lon: float) -> Optional[int]:
        if not self.celulas:
            return None

        linha, coluna = self._celula(lat, lon)
        melhor_no: Optional[int] = None
        melhor_distancia = float("inf")

        # Quanto um anel a mais garante de folga, em metros. A longitude encolhe
        # conforme a latitude, entao usamos o cosseno para nao superestimar.
        folga_por_anel = (
            self.LADO_CELULA_GRAUS * METROS_POR_GRAU * max(math.cos(math.radians(lat)), 0.01)
        )

        for anel in range(self.LIMITE_ANEIS + 1):
            for no_id in self._nos_do_anel(linha, coluna, anel):
                distancia = distancia_haversine(self.coordenadas[no_id], (lat, lon))
                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_no = no_id

            # Todo no ainda nao visitado esta a pelo menos `anel` celulas de
            # distancia. Se o melhor achado ja e mais perto que isso, acabou.
            if melhor_no is not None and melhor_distancia <= anel * folga_por_anel:
                return melhor_no

        return self._buscar_varrendo(lat, lon)

    def _buscar_varrendo(self, lat: float, lon: float) -> Optional[int]:
        melhor_no = None
        melhor_distancia = float("inf")

        for no_id, coord in self.coordenadas.items():
            distancia = distancia_haversine(coord, (lat, lon))
            if distancia < melhor_distancia:
                melhor_distancia = distancia
                melhor_no = no_id

        return melhor_no


@dataclass
class Grafo:
    adjacencia: Dict[int, List[Tuple[int, float]]] = field(default_factory=dict)
    coordenadas: Dict[int, Tuple[float, float]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._indice: Optional[IndiceEspacial] = None

    # O indice e derivado das coordenadas: reconstruimos em vez de gravar no
    # cache, senao o pickle cresceria a toa.
    def __getstate__(self) -> dict:
        return {"adjacencia": self.adjacencia, "coordenadas": self.coordenadas}

    def __setstate__(self, estado: dict) -> None:
        self.adjacencia = estado["adjacencia"]
        self.coordenadas = estado["coordenadas"]
        self._indice = None

    def adicionar_no(self, no_id: int, lat: float, lon: float) -> None:
        if no_id not in self.adjacencia:
            self.adjacencia[no_id] = []
        self.coordenadas[no_id] = (lat, lon)
        self._indice = None

    def adicionar_aresta(self, origem: int, destino: int, peso: float) -> None:
        if origem not in self.adjacencia:
            self.adjacencia[origem] = []
        self.adjacencia[origem].append((destino, peso))

    def vizinhos(self, no_id: int) -> List[Tuple[int, float]]:
        return self.adjacencia.get(no_id, [])

    def no_mais_proximo(self, lat: float, lon: float) -> Optional[int]:
        if self._indice is None:
            self._indice = IndiceEspacial(self.coordenadas)
        return self._indice.buscar(lat, lon)

    def numero_de_nos(self) -> int:
        return len(self.adjacencia)

    def numero_de_arestas(self) -> int:
        return sum(len(v) for v in self.adjacencia.values())

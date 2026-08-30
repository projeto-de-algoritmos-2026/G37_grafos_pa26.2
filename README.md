# G37_grafos_pa26.2 — Rota Mais Rápida (Gama, DF)
**Conteúdo da Disciplina**: Grafos (Algoritmos em Grafos)

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 222006276 | Luís Gustavo Lopes Oliveira |
| 222006211 | Vitor Valerio Hoffmann |

## Sobre
Este projeto é uma aplicação web desenvolvida em **Python** (FastAPI) e
**JavaScript/Leaflet.js** para cálculo de rotas mais rápidas dentro do
Gama-DF, usando dados reais de ruas extraídos do OpenStreetMap.

O sistema modela a malha viária do Gama através de um grafo ponderado, onde
os cruzamentos são os vértices e as ruas são as arestas com pesos baseados
no tempo estimado de deslocamento (distância / velocidade da via).

### Funcionalidades do Sistema:
- **Rota Mínima (Dijkstra)**: encontra a rota de menor tempo entre dois
  pontos clicados no mapa.
- **Dados Reais**: a malha viária do Gama é baixada do OpenStreetMap via
  OSMnx e convertida para uma estrutura de grafo própria.
- **Visualizador Interativo**: mapa em Leaflet.js que desenha a rota
  calculada sobre o mapa real, com origem e destino marcados por clique.

## Estrutura do Projeto
- `backend/`: servidor API FastAPI e algoritmos de grafos (`graph.py`,
  `dijkstra.py`, `graph_loader.py`).
- `frontend/`: interface do usuário em HTML5, CSS e JS (`index.html`,
  `app.js`).
- `run.py`: sobe backend e frontend juntos com um único comando.

## Implementação própria vs. bibliotecas
- **`graph.py`**: estrutura de grafo (lista de adjacência) implementada do
  zero, além da função de distância haversine.
- **`dijkstra.py`**: algoritmo de Dijkstra implementado do zero, usando
  apenas `heapq` (fila de prioridade genérica da biblioteca padrão do
  Python) como estrutura de apoio.
- **`graph_loader.py`**: usa a biblioteca **OSMnx** só para *baixar* os
  dados geográficos reais (cruzamentos, ruas, distâncias) do Gama. Os dados
  baixados são convertidos para a nossa classe `Grafo`; o algoritmo de busca
  nunca roda em cima do grafo do `networkx`, só em cima da nossa estrutura.

## Como Executar
### Pré-requisitos
Python 3.9+ e os pacotes listados em `backend/requirements.txt`.

### Passo a passo
1. Crie e ative um ambiente virtual (evita o erro
   `externally-managed-environment` no Linux):
```bash
python3 -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```
2. Instale as dependências:
```bash
pip install -r backend/requirements.txt
```
3. Suba backend e frontend juntos:
```bash
python run.py
```
Na primeira execução, o download do grafo do Gama via OSMnx pode demorar um
pouco (minutos, dependendo da conexão) — depois disso ele fica salvo em cache
(`backend/gama_cache.pkl`) e carrega instantâneo nas próximas vezes.

4. Acesse a Interface Web:
Abra seu navegador em **[http://127.0.0.1:5500](http://127.0.0.1:5500)**.
A API fica disponível em **[http://127.0.0.1:8000](http://127.0.0.1:8000)**,
com documentação automática em `http://127.0.0.1:8000/docs`.

import CardResultado from "./CardResultado.jsx";

function formatarRegiao(regiao) {
  if (!regiao) return "Distrito Federal";
  return regiao.replace(/,\s*Brazil$/i, "");
}

function formatarCoordenada(ponto) {
  if (!ponto) return null;
  return `${ponto.lat.toFixed(5)}, ${ponto.lng.toFixed(5)}`;
}

function Ponto({ tipo, rotulo, vazio, valor }) {
  return (
    <div className={valor ? "ponto ponto--ativo" : "ponto"}>
      <span className={`ponto__marca ponto__marca--${tipo}`} />
      <div className="ponto__texto">
        <div className="ponto__rotulo">{rotulo}</div>
        <div className="ponto__valor">{valor ?? vazio}</div>
      </div>
    </div>
  );
}

export default function PainelRota({
  origem,
  destino,
  rota,
  carregando,
  erro,
  statusGrafo,
  aoLimpar,
}) {
  const temAlgumPonto = Boolean(origem || destino);

  let instrucao = "Clique no mapa para marcar a origem.";
  if (origem && !destino) instrucao = "Agora clique no destino.";
  if (carregando) instrucao = "Calculando a rota mais rápida…";
  if (rota) instrucao = "Pronto. Clique no mapa para começar outra busca.";

  return (
    <aside className="painel">
      <header className="painel__topo">
        <h1 className="painel__titulo">Rota Mais Rápida</h1>
        <p className="painel__subtitulo">
          {formatarRegiao(statusGrafo?.regiao)} · malha viária do OpenStreetMap
        </p>
      </header>

      <div className="painel__corpo">
        <p className="instrucao">{instrucao}</p>

        <div className="pontos">
          <Ponto
            tipo="origem"
            rotulo="Origem"
            vazio="Não definida"
            valor={formatarCoordenada(origem)}
          />
          <span className="pontos__conector" />
          <Ponto
            tipo="destino"
            rotulo="Destino"
            vazio="Não definido"
            valor={formatarCoordenada(destino)}
          />
        </div>

        {carregando && (
          <div className="carregando">
            <span className="carregando__barra" />
          </div>
        )}

        {erro && <div className="erro">{erro}</div>}

        {rota && !carregando && <CardResultado rota={rota} />}

        <button
          type="button"
          className="botao"
          onClick={aoLimpar}
          disabled={!temAlgumPonto && !erro}
        >
          Limpar
        </button>
      </div>

      <footer className="painel__rodape">
        {statusGrafo ? (
          <>
            <div className="rodape__stat">
              <b>{statusGrafo.nos.toLocaleString("pt-BR")}</b> nós
            </div>
            <div className="rodape__stat">
              <b>{statusGrafo.arestas.toLocaleString("pt-BR")}</b> arestas
            </div>
          </>
        ) : (
          <div className="rodape__stat rodape__stat--offline">
            Aguardando a API… a primeira execução baixa o mapa do DF
          </div>
        )}
      </footer>
    </aside>
  );
}

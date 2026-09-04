function Metrica({ valor, unidade, rotulo, destaque = false }) {
  return (
    <div className={destaque ? "metrica metrica--destaque" : "metrica"}>
      <div className="metrica__valor">
        {valor}
        <span className="metrica__unidade">{unidade}</span>
      </div>
      <div className="metrica__rotulo">{rotulo}</div>
    </div>
  );
}

export default function CardResultado({ rota }) {
  const minutos = rota.tempo_estimado_segundos / 60;

  return (
    <div className="resultado">
      <Metrica
        destaque
        valor={minutos.toFixed(1)}
        unidade="min"
        rotulo="Tempo estimado de viagem"
      />

      <div className="resultado__linha">
        <Metrica
          valor={rota.nos_visitados.toLocaleString("pt-BR")}
          unidade=""
          rotulo="Nós visitados"
        />
        <Metrica
          valor={rota.tempo_calculo_ms.toFixed(1)}
          unidade="ms"
          rotulo="Cálculo do Dijkstra"
        />
      </div>

      <p className="resultado__nota">
        {rota.caminho_coordenadas.length} cruzamentos no caminho encontrado.
      </p>
    </div>
  );
}

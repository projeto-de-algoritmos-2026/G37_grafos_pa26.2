import { useCallback, useEffect, useState } from "react";
import Mapa from "./components/Mapa.jsx";
import PainelRota from "./components/PainelRota.jsx";
import { buscarStatusDoGrafo, calcularRota } from "./api.js";

export default function App() {
  const [origem, setOrigem] = useState(null);
  const [destino, setDestino] = useState(null);
  const [rota, setRota] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState(null);
  const [statusGrafo, setStatusGrafo] = useState(null);

  // Montar o grafo do DF na primeira execucao leva minutos. Em vez de travar
  // em "API offline", ficamos tentando ate o backend responder.
  useEffect(() => {
    let ativo = true;
    let temporizador;

    const consultar = async () => {
      try {
        const status = await buscarStatusDoGrafo();
        if (ativo) setStatusGrafo(status);
      } catch {
        if (ativo) temporizador = setTimeout(consultar, 3000);
      }
    };

    consultar();

    return () => {
      ativo = false;
      clearTimeout(temporizador);
    };
  }, []);

  const limpar = useCallback(() => {
    setOrigem(null);
    setDestino(null);
    setRota(null);
    setErro(null);
    setCarregando(false);
  }, []);

  const aoClicarNoMapa = useCallback(
    async (ponto) => {
      if (carregando) return;

      // Com a rota ja tracada, o proximo clique comeca uma busca nova.
      if (rota || (origem && destino)) {
        setDestino(null);
        setRota(null);
        setErro(null);
        setOrigem(ponto);
        return;
      }

      if (!origem) {
        setOrigem(ponto);
        setErro(null);
        return;
      }

      setDestino(ponto);
      setCarregando(true);
      setErro(null);

      try {
        setRota(await calcularRota(origem, ponto));
      } catch (problema) {
        setErro(problema.message);
        setRota(null);
      } finally {
        setCarregando(false);
      }
    },
    [carregando, rota, origem, destino]
  );

  return (
    <div className="layout">
      <PainelRota
        origem={origem}
        destino={destino}
        rota={rota}
        carregando={carregando}
        erro={erro}
        statusGrafo={statusGrafo}
        aoLimpar={limpar}
      />
      <Mapa
        origem={origem}
        destino={destino}
        rota={rota}
        aoClicarNoMapa={aoClicarNoMapa}
      />
    </div>
  );
}

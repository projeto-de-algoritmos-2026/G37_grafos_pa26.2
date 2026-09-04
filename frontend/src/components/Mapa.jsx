import { useEffect } from "react";
import { MapContainer, Marker, Polyline, TileLayer, useMap, useMapEvents } from "react-leaflet";
import L from "leaflet";

// Centro aproximado do Distrito Federal, com zoom que cobre todas as
// regioes administrativas (Plano Piloto, Gama, Ceilandia, Sobradinho...).
const CENTRO_DF = [-15.78, -47.8];
const ZOOM_INICIAL = 10;

// divIcon evita o problema classico dos icones padrao do Leaflet sumirem
// quando o projeto e empacotado por um bundler.
function criarIcone(tipo) {
  return L.divIcon({
    className: "",
    html: `<span class="pino pino--${tipo}"></span>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11],
  });
}

const ICONE_ORIGEM = criarIcone("origem");
const ICONE_DESTINO = criarIcone("destino");

function CapturadorDeClique({ aoClicarNoMapa }) {
  useMapEvents({
    click: (evento) => aoClicarNoMapa(evento.latlng),
  });
  return null;
}

function AjustarEnquadramento({ rota }) {
  const mapa = useMap();

  useEffect(() => {
    if (!rota?.caminho_coordenadas?.length) return;
    mapa.fitBounds(L.latLngBounds(rota.caminho_coordenadas), {
      paddingTopLeft: [40, 40],
      paddingBottomRight: [40, 40],
    });
  }, [rota, mapa]);

  return null;
}

export default function Mapa({ origem, destino, rota, aoClicarNoMapa }) {
  const traçado = rota?.caminho_coordenadas ?? null;

  return (
    <div className="mapa-area">
      <MapContainer
        center={CENTRO_DF}
        zoom={ZOOM_INICIAL}
        zoomControl={false}
        className="mapa"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        <CapturadorDeClique aoClicarNoMapa={aoClicarNoMapa} />
        <AjustarEnquadramento rota={rota} />

        {/* Duas linhas sobrepostas: a de baixo funciona como contorno da rota. */}
        {traçado && (
          <>
            <Polyline positions={traçado} pathOptions={{ color: "#0b2f6b", weight: 10, opacity: 0.55 }} />
            <Polyline positions={traçado} pathOptions={{ color: "#3b82f6", weight: 5, opacity: 1 }} />
          </>
        )}

        {origem && <Marker position={origem} icon={ICONE_ORIGEM} />}
        {destino && <Marker position={destino} icon={ICONE_DESTINO} />}
      </MapContainer>
    </div>
  );
}

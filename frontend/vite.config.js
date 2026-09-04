import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// O front roda em 5500 e conversa com a API (8000) atraves de um proxy em /api.
// Assim o navegador enxerga tudo na mesma origem e nao dependemos de CORS.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5500,
    strictPort: true,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (caminho) => caminho.replace(/^\/api/, ""),
      },
    },
  },
});

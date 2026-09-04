import shutil
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).parent
BACKEND_DIR = RAIZ / "backend"
FRONTEND_DIR = RAIZ / "frontend"


def encontrar_npm() -> str:
    # No Windows o executavel e npm.cmd; nos demais sistemas e npm.
    for nome in ("npm", "npm.cmd"):
        caminho = shutil.which(nome)
        if caminho:
            return caminho

    print("ERRO: npm nao encontrado. Instale o Node.js (https://nodejs.org).")
    sys.exit(1)


def main():
    npm = encontrar_npm()

    if not (FRONTEND_DIR / "node_modules").exists():
        print("Dependencias do frontend ausentes. Rode primeiro:\n")
        print("    cd frontend && npm install\n")
        sys.exit(1)

    print("Subindo backend (porta 8000) e frontend (porta 5500)...\n")

    processo_backend = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=BACKEND_DIR,
    )

    time.sleep(1)

    processo_frontend = subprocess.Popen(
        [npm, "run", "dev"],
        cwd=FRONTEND_DIR,
    )

    print("\nBackend:  http://127.0.0.1:8000")
    print("Frontend: http://127.0.0.1:5500")
    print("\nCtrl+C para parar os dois.\n")

    try:
        processo_backend.wait()
        processo_frontend.wait()
    except KeyboardInterrupt:
        print("\nEncerrando...")
        processo_backend.terminate()
        processo_frontend.terminate()


if __name__ == "__main__":
    main()

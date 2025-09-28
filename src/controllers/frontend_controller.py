from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from pathlib import Path
import os

from src.app import app, BASE_DIR

FRONTEND_DIR = BASE_DIR / "frontend/pages"
NOT_FOUND_PATH = FRONTEND_DIR / "not_found.html"
INDEX_PATH = FRONTEND_DIR / "index.html"
GAME_PATH = FRONTEND_DIR / "game.html"

def safe_join(base: Path, *paths) -> Path:
    # Prevent directory traversal
    final_path = base.joinpath(*paths).resolve()
    if not str(final_path).startswith(str(base.resolve())):
        return NOT_FOUND_PATH
    return final_path

def serve_content(path: Path ) -> HTMLResponse:
    file_path = path

    with open(file_path, "r") as file:
        content = file.read()

    return HTMLResponse(content=content)

@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
@app.get("/inicio", response_class=HTMLResponse)
def index():
    return serve_content(INDEX_PATH)

@app.get("/contratexto", response_class=HTMLResponse)
@app.get("/game", response_class=HTMLResponse)
def game():
    return serve_content(GAME_PATH)


STATIC_DIR = BASE_DIR / "frontend/pages/assets/"

class SafeStaticFiles(StaticFiles):
    def lookup_path(self, path: str):
        full_path, stat_result = super().lookup_path(path)
        if not full_path or not os.path.exists(full_path):
            # Return NOT_FOUND_PATH if file does not exist
            return str(NOT_FOUND_PATH), None
        return full_path, stat_result

app.mount("/assets", SafeStaticFiles(directory=STATIC_DIR), name="static")
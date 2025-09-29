import os
from pathlib import Path
from dotenv import load_dotenv

import uvicorn

from src.app import app
import src.controllers.runner


ENV = load_dotenv(Path(__file__).parent)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 10000))
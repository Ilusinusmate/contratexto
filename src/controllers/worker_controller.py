import asyncio

from src.app import app, nlp_manager
from src.models.instructions import BaseInstruction
from src.models.responses import BaseResponse, RankResponse
from src.models.player_model import PlayerModel


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(nlp_manager.worker())

import asyncio
from pprint import pprint

from src.app import app, processing_queue, instructor_interpreter, connection_manager, game_state_manager
from src.models.instructions import BaseInstruction
from src.models.responses import BaseResponse, RankResponse
from src.models.player_model import PlayerModel

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker())


async def worker():
    

from fastapi import FastAPI
import asyncio

from src.domain.managers.connection_manager import ConnectionManager
from src.domain.managers.game_manager import GameStateManager
from src.services.instruction_interpreter import InstructionInterpreter
from src.configs import CONFIG

app = FastAPI()
processing_queue: asyncio.Queue = asyncio.Queue()
connection_manager = ConnectionManager()
game_state_manager = GameStateManager(max_points=CONFIG["MAX_POINTS"])
instructor_interpreter = InstructionInterpreter(
    game_manager=game_state_manager,
    connection_manager=connection_manager,
)
from fastapi import FastAPI
import asyncio

from nlp_lib.game_manager import GameManager
from src.domain.managers.connection_manager import ConnectionManager
from src.domain.managers.game_manager import GameStateManager
from src.services.instruction_interpreter import InstructionInterpreter
from src.domain.usecases.game_usecase import GameUsecase
from src.domain.usecases.websocket_usecase import WebsocketUsecase
from src.configs import CONFIG

app = FastAPI()

connection_manager = ConnectionManager()

game_state_manager = GameStateManager(max_points=CONFIG["MAX_POINTS"])

nlp_manager = GameManager(queue_max_size=CONFIG["GAME_MAX_QUEUE_SIZE"])

websocket_usecase = WebsocketUsecase(
    connection_manager=connection_manager,
    game_state_manager=game_state_manager
)

game_usecase = GameUsecase(
    nlp_manager=nlp_manager,
    game_state_manager=game_state_manager,
    websocket_usecase=websocket_usecase
)
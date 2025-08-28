from pydantic import BaseModel
from typing import List

from src.models.player_model import PlayerModel

class BaseResponse(BaseModel):
    connection_id: str
    type: str
    status: bool

class SetNameResponse(BaseResponse):
    type: str = "SET_NAME"
    new_nick_name: str

class WordPositionResponse(BaseResponse):
    type: str = "WORD"
    word: str
    position: int

class FrozenResponse(BaseResponse):
    type: str = "FROZEN"

class RankResponse(BaseResponse):
    type: str = "RANK"
    rank: List[PlayerModel]
    
class WinnerResponse(BaseResponse):
    type:str = "WINNER"
    player: PlayerModel

class ErrorResponse(BaseResponse):
    type: str = "ERROR"
    status: bool = False
    error: str

class LoginResponse(BaseResponse):
    status: bool = True
    type: str = "LOGIN"
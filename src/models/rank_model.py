from pydantic import BaseModel
from typing import List

from src.models.player_model import PlayerModel

class RankTable(BaseModel):
    table: List[PlayerModel]
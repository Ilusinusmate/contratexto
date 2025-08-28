from pydantic import BaseModel
from typing import List

from player_model import PlayerModel

class RankTable(BaseModel):
    table: List[PlayerModel]
    last_words: List[str]
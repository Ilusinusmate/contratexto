from pydantic import BaseModel
from typing import List

class PlayerModel(BaseModel):
    nick_name: str
    connection_id: str
    points: int
    is_frozen: bool





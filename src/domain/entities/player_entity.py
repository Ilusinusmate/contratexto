from src.configs import CONFIG
from datetime import datetime, timezone, timedelta
from random import randint

from src.models.player_model import PlayerModel

class PlayerEntity():
    def __init__(
        self,
        connection_id: str,
        nick_name: str = f"user{randint(0, 50)}",
        points: int = 0,
        perks_used: int = CONFIG["MAX_PERKS"],
        last_frozen: datetime = datetime.now(timezone.utc)+timedelta(minutes=10),
        best_word_position: int | None = None
    ):
        self.connection_id: str = connection_id 
        self.points: int = points
        self.nickname: str = nick_name
        self.perks_used: int = perks_used
        self.last_frozen: datetime = last_frozen
        self.best_word_position: int | None = best_word_position

    def increment_points(self, ammount: int = 1):
        self.points += ammount

    def change_nickname(self, new_nickname: str):
        self.nickname = new_nickname

    def use_perk(self):
        self.perks_used = max(self.perks_used -1, 0)

    def can_use_perk(self) -> bool:
        return self.perks_used <= 0

    def is_frozen(self) -> bool:
        (datetime.now(timezone.utc)- self.last_frozen) < CONFIG["FROZEN_TIME"]
    
    def freeze(self):
        self.last_frozen = datetime.now(timezone.utc)

    def set_best_word_pos(self, position: int):
        self.best_word_position = min(position, self.best_word_position)

    def to_model(self) -> PlayerModel:
        PlayerModel(
            connection_id=self.connection_id,
            is_frozen=self.is_frozen(),
            nick_name=self.nickname,
            points=self.points,
            best_word_position=self.best_word_position
        )
        
from src.configs import CONFIG
from datetime import datetime, timezone, timedelta
from random import randint

from src.models.player_model import PlayerModel

class PlayerEntity():
    def __init__(
        self,
        nick_name: str = f"user{randint(0, 50)}",
        points: int = 0,
        perks_used: int = CONFIG["MAX_PERKS"],
        last_frozen: datetime = datetime.now(timezone.utc)+timedelta(minutes=10),
    ):
        self.points: int = points
        self.nick_name: str = nick_name
        self.perks_used: int = perks_used
        self.last_frozen: datetime = last_frozen

    def increment_points(self, ammount: int = 1):
        self.points += ammount

    def change_nick_name(self, new_nick_name: str):
        self.nick_name = new_nick_name

    def use_perk(self):
        self.use_perk = max(self.use_perk -1, 0)

    def can_use_perk(self) -> bool:
        return self.perks_used <= 0

    def is_frozen(self) -> bool:
        (datetime.now(timezone.utc)- self.last_frozen) < CONFIG["FROZEN_TIME"]
    
    def freeze(self):
        self.last_frozen = datetime.now(timezone.utc)

    def to_model(self) -> PlayerModel:
        PlayerModel(
            connection_id="",
            is_frozen=self.is_frozen(),
            nick_name=self.nick_name,
            points=self.points,
        )
        
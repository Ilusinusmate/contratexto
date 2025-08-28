from src.domain.entities.player_entity import PlayerEntity
from typing import Dict, List

class GameStateManager():
    def __init__(self, max_points: int):
        self.players: Dict[str, PlayerEntity] = {}
        self.max_points = max_points

    def add_player(self, connection_id: str, player: PlayerEntity) -> None:
        self.players[connection_id] = player
    
    def remove_player(self, connection_id: str) -> None:
        if connection_id in self.players:
            del self.players[connection_id]

    def increment_points(self, connection_id: str, ammount: int = 1) -> None:
        if connection_id in self.players:
            self.players[connection_id].increment_points(ammount)

    def has_winner(self) -> PlayerEntity | None:
        for player in self.players.values():
            if player.points >= self.max_points:
                return player

    def get_rank(self) -> List[PlayerEntity]:
        return sorted(
            self.players.values(),
            key=lambda x : x.points,
            reverse=True,
        )

    def is_player_frozen(self, connection_id: str) -> bool:
        if connection_id in self.players:
            return self.players[connection_id].is_frozen()

    def freeze_player(self, connection_id: str) -> None:
        if connection_id in self.players:
            self.players[connection_id].freeze()

    def can_use_perk(self, connection_id: str) -> bool:
        if connection_id in self.players:
            return self.players[connection_id].can_use_perk()
        
    def use_perk(self, connection_id: str) -> None:
        if connection_id in self.players:
            self.players[connection_id].use_perk()

    def set_player_name(self, connection_id: str, player_name: str) -> None:
        if connection_id in self.players:
            self.players[connection_id].change_nick_name(player_name)

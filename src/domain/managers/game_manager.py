from src.domain.entities.player_entity import PlayerEntity
from typing import Dict, List

class GameStateManager():
    def __init__(self, max_points: int):
        self.players: Dict[str, PlayerEntity] = {}
        self.best_actual_rank: Dict[str, int | None] = {}
        self.max_points = max_points

    @staticmethod
    def calculate_hint_pos(pos: int) -> int:
        if pos >= 3: return 2
        return pos // 2

    def add_player(self, connection_id: str, player: PlayerEntity) -> None:
        self.players[connection_id] = player
    
    def remove_player(self, connection_id: str) -> None:
        if connection_id in self.players:
            del self.players[connection_id]

    def get_player(self, connection_id: str) -> PlayerEntity | None:
        return self.players.get(connection_id, None)

    def set_player_nickname(self, connection_id: str, new_nickname: str) -> bool:
        if connection_id in self.players:
            return False
        
        for player in self.players.values():
            if player.nickname == new_nickname: return False
        
        player.change_nickname(new_nickname)
        return True

    def increment_points(self, connection_id: str, ammount: int = 1) -> None:
        if connection_id in self.players:
            self.players[connection_id].increment_points(ammount)

    def has_winner(self) -> PlayerEntity | None:
        for player in self.players.values():
            if player.points >= self.max_points:
                return player
            
    def is_winner(self, player_connection_id: str) -> bool:
        return self.players[player_connection_id].points >= self.max_points
                
    def get_points_rank(self) -> List[PlayerEntity]:
        return sorted(
            self.players.values(),
            key = lambda x : x.points,
            reverse = True,
        )
    
    def get_words_rank(self) -> List[str]:
        return [
            element[0] for element in 
            sorted(
                self.best_actual_rank.items(),
                key = lambda x: x[1]
            )
        ]

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

    def set_player_rank_pos(self, connection_id: str, position: int) -> None:
        if connection_id in self.best_actual_rank and connection_id in self.players:
            self.best_actual_rank[connection_id] = min(position, self.best_actual_rank[connection_id])
            self.players[connection_id].set_best_word_pos(position)

    def get_player_rank_pos(self, connection_id: str) -> int | None:
        return self.best_actual_rank.get(connection_id, None)

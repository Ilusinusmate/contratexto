from src.domain.managers.connection_manager import ConnectionManager
from src.domain.managers.game_manager import GameStateManager
from src.models.responses import WinnerResponse
from src.models.rank_model import RankTable
from src.domain.entities.player_entity import PlayerEntity

class WebsocketUsecase():
    def __init__(
        self,
        game_state_manager: GameStateManager,
        connection_manager: ConnectionManager
    ):
        self.game_manager = game_state_manager
        self.connection_manager = connection_manager


    async def check_user_winned(self, player: PlayerEntity):
        if not self._has_winned(player):
            return
        
        self.game_manager.increment_points(
            player.connection_id
        )

        await self.connection_manager.broadcast(
            WinnerResponse(
                player=player.nickname,
            ).model_dump()
        )
        

    def _has_winned(self, player: PlayerEntity) -> bool:
        return self.game_manager.is_winner(player.connection_id)
    

    async def broad_cast_rank(self) -> None:
        self.connection_manager.broadcast(
            RankTable(
                table=list(
                    map(
                        lambda x: x.to_model(),
                        self.game_manager.players.values()
                    )
                )
            ).model_dump()
        )


    

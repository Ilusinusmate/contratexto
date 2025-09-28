from src.domain.managers.connection_manager import ConnectionManager
from src.domain.managers.game_manager import GameStateManager
from src.models.responses import GameWinnerResponse, RoundWinnerResponse
from src.models.rank_model import RankTable
from src.domain.entities.player_entity import PlayerEntity
from nlp_lib.game_manager import GameManager

class WebsocketUsecase():
    def __init__(
        self,
        game_state_manager: GameStateManager,
        connection_manager: ConnectionManager,
        nlp_manager: GameManager
    ):
        self.game_state_manager = game_state_manager
        self.connection_manager = connection_manager
        self.nlp_manager = nlp_manager


    async def check_user_winned_game(self, player: PlayerEntity) -> None:
        if not self._has_winned_game(player):
            return

        await self.connection_manager.broadcast(
            GameWinnerResponse(
                player=player,
            ).model_dump()
        )
        
        self.game_state_manager.reset_rank()
        

    async def check_user_winned_round(self, player: PlayerEntity, word_position: int):
        if (word_position != 1): return

        await self.connection_manager.broadcast(
            RoundWinnerResponse(
                player=player,
            ).model_dump()
        )

        self.game_state_manager.increment_points(
            player.connection_id
        )

        self.nlp_manager.end_game()

        

    def _has_winned_game(self, player: PlayerEntity) -> bool:
        return self.game_state_manager.is_winner(player.connection_id)
    

    async def broad_cast_rank(self) -> None:
        await self.connection_manager.broadcast(
            RankTable(
                table=list(
                    map(
                        lambda x: x.to_model(),
                        self.game_state_manager.players.values()
                    )
                )
            ).model_dump()
        )


    

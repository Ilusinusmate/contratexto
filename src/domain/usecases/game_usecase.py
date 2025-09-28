from typing import Awaitable
from fastapi import BackgroundTasks
from functools import wraps

from nlp_lib.game_class import Contratexto
from nlp_lib.game_manager import GameManager
from src.domain.managers.game_manager import GameStateManager
from src.models.responses import WordPositionResponse, FrozenResponse,FreezeReponse, ErrorResponse, SetNameResponse
from src.domain.entities.player_entity import PlayerEntity
from src.domain.usecases.websocket_usecase import WebsocketUsecase

class GameUsecase():
    def __init__(self, game_state_manager, nlp_manager, websocket_usecase):
        self.manager: GameStateManager = game_state_manager
        self.nlp_manager: GameManager = nlp_manager
        self.websockect_usecase: WebsocketUsecase = websocket_usecase



    async def _get_game(self) -> Awaitable[Contratexto]:
        return await self.nlp_manager.get_game()



    async def _finalize_round(self, player: PlayerEntity, check_winner: bool = True) -> None:
        if check_winner:
            await self.websockect_usecase.check_user_winned_game(player)
        await self.websockect_usecase.broad_cast_rank()



    def check_frozen(func):
        @wraps(func)
        async def wrapper(self, player: PlayerEntity, *args, **kwargs):
            if self.manager.is_player_frozen(player.connection_id):
                return FrozenResponse(connection_id=player.connection_id)
            return await func(self, player, *args, **kwargs)
        return wrapper



    def check_perks_available(func):
        @wraps(func)
        async def wrapper(self, player: PlayerEntity, *args, **kwargs):
            if not self.manager.can_use_perk(player.connection_id):
                return ErrorResponse(
                    connection_id=player.connection_id,
                    error="No more perks available"
                )
            return await func(self, player, *args, **kwargs)
        return wrapper



    def get_player_by_connection_id(self, connection_id: str) -> PlayerEntity | None:
        return self.manager.get_player(connection_id=connection_id)



    async def set_player_nickname(
        self,
        player: PlayerEntity,
        background_tasks: BackgroundTasks,
        new_nickname: str
    ) -> SetNameResponse | ErrorResponse:
        
        if self.manager.set_player_nickname(player, new_nickname):
            return SetNameResponse(
                connection_id=player.connection_id,
                new_nickname=new_nickname,
            )
        

        background_tasks.add_task(self._finalize_round, player, False)
        return ErrorResponse(
            connection_id=player.connection_id,
            error="Nicknames must be uniques!"
        )



    @check_frozen
    async def guess_word(
        self, player: PlayerEntity,
        background_tasks: BackgroundTasks,
        word: str
    ) -> FrozenResponse | WordPositionResponse:

        game: Contratexto = await self._get_game()
        position = game.guess_word(word)

        self.manager.set_player_rank_pos(
            player.connection_id,
            position=position
        )

        await self.websockect_usecase.check_user_winned_round(
            player=player,
            word_position=position
        )

        background_tasks.add_task(self._finalize_round, player)
        return WordPositionResponse(
            connection_id=player.connection_id,
            position=position,
            word=word,
        )
    


    @check_frozen
    @check_perks_available
    async def freeze_player(
        self,
        player: PlayerEntity,
        background_tasks: BackgroundTasks,
        target_id: str
    ) -> FrozenResponse | FreezeReponse | ErrorResponse:



        result = self.manager.freeze_player(target_id)
        
        if not result:
            return ErrorResponse(
                connection_id=player.connection_id,
                error="Was not possible to Freeze this player."
            )
        
        self.manager.use_perk(player.connection_id)
        background_tasks.add_task(self._finalize_round, player, False)
        return FreezeReponse(
            connection_id=player.connection_id,
        )
        


    @check_frozen
    @check_perks_available
    async def ask_hint(
        self,
        player: PlayerEntity,
        background_tasks: BackgroundTasks
    ) -> FrozenResponse | ErrorResponse | WordPositionResponse:

        position = self.manager.get_player_rank_pos(player.connection_id)
        game: Contratexto = await self._get_game()

        if position == None: return ErrorResponse(
            connection_id=player.connection_id,
            error="Guess a word first. Then ask hints!"
        )

        position = self.manager.calculate_hint_pos(position)
        
        word = game.get_word_in_position(position)

        self.manager.set_player_rank_pos(
            player.connection_id,
            position=position
        )

        self.manager.use_perk(
            connection_id=player.connection_id
        )

        background_tasks.add_task(self._finalize_round, player)
        return WordPositionResponse(
            connection_id=player.connection_id,
            position=position,
            word=word,
        )




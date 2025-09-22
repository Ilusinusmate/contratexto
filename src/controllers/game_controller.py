from typing import Annotated, Union
from fastapi import Query, HTTPException, status, Depends

from src.domain.entities.player_entity import PlayerEntity
from src.models.responses import WordPositionResponse, FrozenResponse, SetNameResponse, ErrorResponse
from src.app import app, game_usecase
from src.domain.usecases.game_usecase import GameUsecase


def check_connection_id(connection_id: str = Query(...)):
    player = game_usecase.get_player_by_connection_id(connection_id)

    if player == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Connection ID"
        )
    
    return player


@app.get("/ask-hint", response_model=Union[ErrorResponse, WordPositionResponse, FrozenResponse])
async def ask_hint(
    *,
    player: Annotated[PlayerEntity, Depends(check_connection_id)],    
):
    response = await game_usecase.ask_hint(
        player=player
    )

    response.connection_id = player.connection_id
    return response


@app.post("/freeze", response_model=Union[FrozenResponse, ErrorResponse])
async def freeze_player(
    *,
    player: Annotated[PlayerEntity, Depends(check_connection_id)],    
    target_id: str,
):
    response = await game_usecase.freeze_player(
        player=player,
        target_id=target_id
    )

    response.connection_id = player.connection_id
    return response
    

@app.post("/words", response_model=Union[WordPositionResponse, FrozenResponse])
async def guess_word(
    *,
    player: Annotated[PlayerEntity, Depends(check_connection_id)],
    word: str,    
):
    response = await game_usecase.guess_word(
        player=player,
        word=word
    )

    response.connection_id = player.connection_id
    return response


@app.post("/set-name", response_model=Union[ErrorResponse, SetNameResponse])
async def set_nickname(
    *,
    player: Annotated[PlayerEntity, Depends(check_connection_id)],
    new_nickname: str,    
):
    response = await game_usecase.set_player_nickname(
        player=player,
        new_nickname=new_nickname
    )

    response.connection_id = player.connection_id
    return response


    


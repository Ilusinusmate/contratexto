from fastapi import WebSocket, WebSocketDisconnect, BackgroundTasks
import asyncio

from src.app import app, connection_manager, game_state_manager, websocket_usecase
from src.models.responses import LoginResponse, RankResponse
from src.domain.entities.player_entity import PlayerEntity

async def send_connection_id(connection_id: str):
    await connection_manager.send_personal_json(
        LoginResponse(connection_id=connection_id).model_dump(),
        connection_id
    )
    await websocket_usecase.broad_cast_rank()


@app.websocket("/ws")
async def connect_websocket(
    websocket: WebSocket,
    bacground_tasks: BackgroundTasks
):
    connection_id: str = await connection_manager.connect(websocket)
    
    game_state_manager.add_player(
        connection_id=connection_id,
        player=PlayerEntity(
            connection_id=connection_id,
            nick_name=f"User-{len(game_state_manager.players)+1}",
            points=0,
        )
    )

    asyncio.create_task(send_connection_id(connection_id))

    try: 
        while True:
            await websocket.receive_bytes()

    except WebSocketDisconnect:
        connection_manager.disconnect(connection_id)
        game_state_manager.remove_player(connection_id)
        await websocket_usecase.broad_cast_rank()



from fastapi import WebSocket, WebSocketDisconnect

from src.app import app, connection_manager, processing_queue
from src.models.responses import LoginResponse

@app.websocket("/ws")
async def connect_websocket(
    websocket: WebSocket
):
    connection_id: str = await connection_manager.connect(websocket)
    await connection_manager.send_personal_json(
        LoginResponse(connection_id=connection_id).dict(),
        connection_id
    )

    try: 
        while True:
            continue

    except WebSocketDisconnect:
        connection_manager.disconnect(connection_id)

    



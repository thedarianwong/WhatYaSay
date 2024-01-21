from fastapi import APIRouter, WebSocket
import io

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")

        data = await websocket.receive_bytes()
        await websocket.send_bytes(data)
        with open("test_audio.webm", "ab") as file:
            file.write(data)




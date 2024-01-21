from fastapi import APIRouter, WebSocket
import io

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")

    # while True:
    #     data = await websocket.receive_text()
    #     await websocket.send_text(f"Message received: {data}")

    while True:
        try:
            data = await websocket.receive_bytes()
            print(f"Received data: {data[:30]}...")  # Print first few bytes for brevity
            await websocket.send_bytes(data)
            with open("test_audio.webm", "ab") as file:
                file.write(data)
        except Exception as e:
            print(f"Error: {e}")
            break

    print("WebSocket connection closed")




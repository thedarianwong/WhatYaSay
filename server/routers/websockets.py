from fastapi import APIRouter, WebSocket
from services.speech import transcribe_streaming
import io
import asyncio

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # print("WebSocket connection established")

    # Buffer to store incoming audio data
    audio_buffer = io.BytesIO()

    while True:
        try:
            data = await websocket.receive_bytes()
            await audio_buffer.write(data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


    # Process the accumulated audio data for transcription
    audio_content = await audio_buffer.getvalue()
    await audio_buffer.close()
    await websocket.send_text(transcribe_streaming(audio_content))
    # try:
    #     while True:
    #         await websocket.send_text("Hello")
    #         await asyncio.sleep(2)  # Wait for 2 seconds before sending the next message
    # except Exception as e:
    #     print(f"WebSocket connection error: {e}")
    # finally:
    #     print("WebSocket connection closed")
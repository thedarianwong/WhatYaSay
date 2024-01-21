from fastapi import APIRouter, WebSocket
from services.speech import transcribe_streaming, receive_audio_chunks

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")
    
    audio_stream = receive_audio_chunks(websocket)
    await transcribe_streaming(audio_stream)

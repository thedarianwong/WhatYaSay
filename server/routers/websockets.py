from fastapi import APIRouter, WebSocket
from services.speech import transcribe
from google.cloud import speech
import io
import asyncio

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connection_closed = False  # Flag to track the connection status
    try:
        # Initialize an empty bytes object to accumulate the data
        data = b''

        # Receive data in chunks from the WebSocket
        while True:
            message = await websocket.receive_bytes()
            if message == b'end':  # You can define a protocol for the end of the message
                break
            data += message
            audio_content = speech.RecognitionAudio(content=data)

            # Transcribe the audio and get the response
            response = await transcribe(audio_content)

            # Send the transcription result back to the client
            await websocket.send_text("Transcription: " + str(response))

    except Exception as e:
        print(f"Error receiving data here: {e}")
    finally:
        if not connection_closed:
            await websocket.close()
            connection_closed = True  # Update the flag after closing
            print("WebSocket connection closed")

    # try:
    #     while True:
    #         await websocket.send_text("Hello")
    #         await asyncio.sleep(2)  # Wait for 2 seconds before sending the next message
    # except Exception as e:
    #     print(f"WebSocket connection error: {e}")
    # finally:
    #     print("WebSocket connection closed")
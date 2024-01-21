import asyncio
from google.oauth2 import service_account
from google.cloud import speech

# Initialize the Google Cloud client with credentials
client_file = 'whatyasay.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

async def transcribe_streaming(audio_stream):
    """
    Transcribe streaming audio data.
    """
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        enable_speaker_diarization=True,
        diarization_speaker_count=2
        # Add additional configuration as needed
    )

    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_stream)

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")
            for word_info in result.alternatives[0].words:
                print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")
    return responses

async def receive_audio_chunks(websocket):
    while True:
        try:
            chunk = await websocket.receive_bytes()
            if not chunk:
                break  # Handle the end of the stream
            yield chunk
        except Exception as e:
            print(f"Error receiving audio chunk: {e}")
            break
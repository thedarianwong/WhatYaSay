import asyncio
from google.oauth2 import service_account
from google.cloud import speech

# Initialize the Google Cloud client with credentials
try:
    client_file = 'services/whatyasaya.json'
except:
    print("Add whatyasay.json under this dir")
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

async def transcribe_streaming(audio_stream):
    """
    Transcribe streaming audio data.
    """
    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=10,
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        enable_automatic_punctuation=True,
        language_code="en-US",
        diarization_config=diarization_config,
        sample_rate_hertz = 48000,
    )

    streaming_config = await speech.StreamingRecognitionConfig(config=config, interim_results=True)

    requests = await (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_stream)

    responses = await client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")
            for word_info in result.alternatives[0].words:
                print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")
    return responses
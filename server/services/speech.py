import io
from google.oauth2 import service_account
from google.cloud import speech

def transcribe(audio) -> speech.RecognizeResponse:
    """
    Transcribe the given audio file asynchronously and output the word time
    offsets.
    """
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)

    for result in result.results:
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")
        print(f"Confidence: {alternative.confidence}")

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )

    return result

try:
    client_file = 'whatyasay'
except:
    print("Add whatyasay.json under this dir")
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

# Load the audio file
audio_file = 'sample_audio.wav'
with io.open(audio_file, 'rb') as f:
    content = f.read()
    audio = speech.RecognitionAudio(content=content)
    transcribe(audio)
import io
from google.oauth2 import service_account
from google.cloud import speech


def transcribe(audio) -> speech.RecognizeResponse:
    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=10,
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        language_code="en-US",
        diarization_config=diarization_config,
        audio_channel_count = 1,
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)
    result = response.results[-1]

    words_info = result.alternatives[0].words
    for word_info in words_info:
        print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")

    return result

try:
    client_file = 'whatyasay.json'
except:
    print("Add whatyasay.json under this dir")
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

# Load the audio file
audio_file = 'sample_audio.wav'
with io.open(audio_file, 'rb') as f:
    content = f.read()
    audio = speech.RecognitionAudio(content=content)
    transcribe(audio=audio)
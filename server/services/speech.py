import io
from google.oauth2 import service_account
from google.cloud import speech
import wave

def transcribe(audio, frame_rate, channel_count) -> speech.RecognizeResponse:
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
        audio_channel_count = channel_count,
        sample_rate_hertz = frame_rate,
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)
    result = response.results[-1]

    words_info = result.alternatives[0].words
    for word_info in words_info:
        print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")

    return result

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channel_count = wave_file.getnchannels()
        return frame_rate,channel_count
    
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
    frame_rate,channel_count = frame_rate_channel(audio_file_name=audio_file)
    transcribe(audio=audio, frame_rate=frame_rate, channel_count=channel_count)
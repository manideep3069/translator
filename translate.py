import os
from gtts import gTTS
from speechmatics.models import ConnectionSettings
from speechmatics.batch_client import BatchClient
from httpx import HTTPStatusError

# Supported input and output languages
LANGUAGES = {
    "bg": "bulgarian",
    "ca": "catalan",
    "zh-cn": "chinese (simplified)",
    "hr": "croatian",
    "cs": "czech",
    "da": "danish",
    "nl": "dutch",
    "en": "english",
    "et": "estonian",
    "fi": "finnish",
    "fr": "french",
    "gl": "galician",
    "de": "german",
    "el": "greek",
    "hi": "hindi",
    "hu": "hungarian",
    "id": "indonesian",
    "it": "italian",
    "ja": "japanese",
    "ko": "korean",
    "lv": "latvian",
    "lt": "lithuanian",
    "ms": "malay",
    "no": "norwegian",
    "pl": "polish",
    "pt": "portuguese",
    "ro": "romanian",
    "ru": "russian",
    "sk": "slovak",
    "sl": "slovenian",
    "es": "spanish",
    "sv": "swedish",
    "tr": "turkish",
    "uk": "ukrainian",
    "vi": "vietnamese",
}

# Function to translate and create audio file
def translate_and_speak(input_text, input_language, output_language):
    # Get Speechmatics API key from environment variable
    API_KEY = os.environ.get("SPEECHMATICS_API_KEY")
    if not API_KEY:
        raise ValueError("SPEECHMATICS_API_KEY environment variable not set!")

    # Perform transcription and translation using Speechmatics
    settings = ConnectionSettings(
        url="https://asr.api.speechmatics.com/v2",
        auth_token=API_KEY,
    )

    conf = {
        "type": "transcription",
        "transcription_config": {
            "language": input_language
        },
        "translation_config": {
            "target_languages": [output_language]
        }
    }

    # Open the client using a context manager
    with BatchClient(settings) as client:
        try:
            # Submit the job using the provided text
            job_id = client.submit_job(
                content=input_text,
                transcription_config=conf,
            )

            # Wait for the transcription to complete
            transcript = client.wait_for_completion(job_id, transcription_format='json-v2')

            translation = ""
            for translated_segment in transcript["translations"][output_language]:
                translation += translated_segment["content"] + " "

            # Create an audio file from the translated text
            audio_file = "translated_audio.mp3"
            tts = gTTS(text=translation, lang=output_language)
            tts.save(audio_file)

            # Return the translation and the path to the audio file
            return translation, audio_file

        except HTTPStatusError as e:
            if e.response.status_code == 401:
                return 'Invalid API key - Check your SPEECHMATICS_API_KEY secret!', None
            elif e.response.status_code == 400:
                return e.response.json()['detail'], None
            else:
                raise e

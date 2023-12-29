from gtts import gTTS
from playsound import playsound
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
# Function to translate and speak
def translate_and_speak(input_text, input_language, output_language):
    # Set your Speechmatics API key
    API_KEY = "zFxoWhVGjWGi8fMIzw0ZNF7fhng2v8zA"

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
            print(f'Job {job_id} submitted successfully, waiting for transcript')

            # Wait for the transcription to complete
            transcript = client.wait_for_completion(job_id, transcription_format='json-v2')

            for language in [output_language]:
                # Print the translation for the selected output language from the JSON
                print(f"Translation for {language}")
                translation = ""
                for translated_segment in transcript["translations"][language]:
                    translation += translated_segment["content"] + " "
                print(translation)

                # Create an audio file from the translated text
                tts = gTTS(text=translation, lang=output_language)
                tts.save("translated_audio.mp3")

                # Play the translated audio
                playsound("translated_audio.mp3")

                # Return the translation result (Gradio requires a return value)
                return translation

        except HTTPStatusError as e:
            if e.response.status_code == 401:
                print('Invalid API key - Check your API_KEY at the top of the code!')
            elif e.response.status_code == 400:
                print(e.response.json()['detail'])
            else:
                raise e


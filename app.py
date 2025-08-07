import gradio as gr
from translate import translate_and_speak, LANGUAGES

def translation_interface(input_text, input_language, output_language):
    if not input_text:
        return "Please enter text to translate.", None
    try:
        translation, audio_file = translate_and_speak(input_text, input_language, output_language)
        return translation, audio_file
    except ValueError as e:
        return str(e), None

# Create the Gradio interface
iface = gr.Interface(
    fn=translation_interface,
    inputs=[
        gr.Textbox(lines=5, label="Text to Translate"),
        gr.Dropdown(list(LANGUAGES.keys()), label="Input Language", value="en"),
        gr.Dropdown(list(LANGUAGES.keys()), label="Output Language", value="fr"),
    ],
    outputs=[
        gr.Textbox(label="Translated Text"),
        gr.Audio(label="Translated Audio"),
    ],
    title="Live Translation",
    description="Enter text and select languages for translation. The translated text and audio will be provided.",
    allow_flagging="never",
)

# Launch the app
iface.launch()

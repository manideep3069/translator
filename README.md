---
title: Live Translation
emoji: 🌍
colorFrom: green
colorTo: blue
sdk: gradio
python_version: 3.12
sdk_version: 4.19.2
app_file: app.py
secrets:
  - SPEECHMATICS_API_KEY
---

# Live Translation

This is a live translation application that uses Speechmatics for transcription and translation, and gTTS for text-to-speech.

## How to use

1.  Enter the text you want to translate in the "Text to Translate" box.
2.  Select the input language from the "Input Language" dropdown.
3.  Select the output language from the "Output Language" dropdown.
4.  The translated text will appear in the "Translated Text" box, and you can listen to the translated audio.

## Setup

To run this application, you need to add your Speechmatics API key as a secret to this Hugging Face Space.

1.  Go to the "Settings" tab of your Space.
2.  Under "Secrets", add a new secret with the name `SPEECHMATICS_API_KEY` and your API key as the value.

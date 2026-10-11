
import sounddevice as sd
import numpy as np
import speech_recognition as sr

from commands.basic_commands import process_command
from voice.text_to_speech import speak


# Microphone settings
DURATION = 5
SAMPLE_RATE = 44100
DEVICE = 1


def listen_for_command():
    """Record audio and return the recognized text."""

    print("SAMSHIV is listening...")
    print("Please speak...")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=DEVICE
    )

    sd.wait()

    print("Recording finished!")

    # Convert float audio into 16-bit integer audio
    audio_int16 = (recording * 32767).astype(np.int16)
    audio_bytes = audio_int16.tobytes()

    audio = sr.AudioData(
        audio_bytes,
        SAMPLE_RATE,
        2
    )

    recognizer = sr.Recognizer()

    try:
        print("Converting speech to text...")

        text = recognizer.recognize_google(audio)

        print("You said:", text)
        return text

    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
        return None

    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        print("Check your internet connection.")
        return None


def listen_and_respond():
    """Listen, process a command, and speak the response."""

    text = listen_for_command()

    if not text:
        return None

    response = process_command(text)

    print("SAMSHIV:", response)

    if response:
        speak(str(response))

    return text
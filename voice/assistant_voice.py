import sounddevice as sd
import numpy as np
import speech_recognition as sr

from commands.basic_commands import process_command
from voice.text_to_speech import speak


# Microphone settings
duration = 5
sample_rate = 44100
device = 1


def listen_and_respond():

    print("JARVIS is listening...")
    print("Please speak...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        device=device
    )

    sd.wait()

    print("Recording finished!")
    print("Converting audio...")

    # Convert audio to SpeechRecognition format
    audio_int16 = (recording * 32767).astype(np.int16)
    audio_bytes = audio_int16.tobytes()

    audio = sr.AudioData(
        audio_bytes,
        sample_rate,
        2
    )

    recognizer = sr.Recognizer()

    print("Converting speech to text...")

    try:

        text = recognizer.recognize_google(audio)

        print("You said:", text)

        response = process_command(text)

        print("JARVIS:", response)

        speak(response)

        return text

    except sr.UnknownValueError:

        print("Sorry, I could not understand your voice.")
        return None

    except sr.RequestError:

        print("Speech recognition service is unavailable.")
        print("Check your internet connection.")
        return None

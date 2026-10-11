
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):
    if not text:
        return

    engine.say(str(text))
    engine.runAndWait()


if __name__ == "__main__":
    speak(
        "Hey! I'm JARVIS. "
        "I'm here to help you learn, build projects, "
        "and solve problems. What shall we do today?"
    )
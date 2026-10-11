# JARVIS - Personal AI Voice Assistant

JARVIS is a Python-based personal AI voice assistant designed to interact with the user through voice commands.

This project is being developed as a practical learning project to understand Python, Artificial Intelligence, speech recognition, text-to-speech, automation, APIs, and software development using Git and GitHub.

## 🚀 Features

- 🎤 Voice input through microphone
- 🗣️ Speech recognition
- 🔊 Text-to-speech responses
- 🤖 AI-powered question answering
- 💬 Basic conversational interaction
- 📝 Notes management
- ✅ Task management
- ⏰ Reminder management
- 🎵 Music and YouTube control
- 💻 Windows system controls
- 🕒 Time and date commands
- 🌦️ Weather-related commands
- 🔧 Modular Python project structure

## 🛠️ Technologies Used

- Python
- SpeechRecognition
- SoundDevice
- NumPy
- pyttsx3
- OpenAI Python SDK
- python-dotenv
- LLM7 API
- Git
- GitHub

## 📂 Project Structure

```text
JARVIS/
│
├── ai/
│   └── llm.py
│
├── commands/
│   ├── basic_commands.py
│   └── router.py
│
├── core/
│   ├── assistant.py
│   ├── conversation.py
│   ├── notes.py
│   ├── reminder.py
│   ├── tasks.py
│   ├── time_parser.py
│   └── system_control.py
│
├── music/
│
├── tests/
│   └── test_llm.py
│
├── voice/
│   ├── assistant_voice.py
│   ├── microphone_test.py
│   └── text_to_speech.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
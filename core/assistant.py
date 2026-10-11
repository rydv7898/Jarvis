
from voice.assistant_voice import listen_and_respond
from commands.basic_commands import process_command
from core.memory import ConversationMemory


def start_assistant():
    print("SAMSHIV assistant loop started.")

    memory = ConversationMemory(max_messages=10)

    while True:
        print("\nSAMSHIV is ready for the next command...")

        # Listen to the user
        text = listen_and_respond()

        if text is None:
            continue

        command = text.lower().strip()

        # Exit commands
        if command in ("stop", "exit", "quit", "goodbye") or (
            "stop assistant" in command
            or "close samshiv" in command
        ):
            print("SAMSHIV: Goodbye Sam!")
            break


if __name__ == "__main__":
    start_assistant()
from voice.assistant_voice import listen_and_respond


def start_assistant():

    print("JARVIS assistant loop started.")

    while True:

        print("\nJARVIS is ready for the next command...")

        text = listen_and_respond()

        if text is None:
            continue

        command = text.lower().strip()

        if (
            command == "stop"
            or command == "exit"
            or "stop assistant" in command
            or "close JARVIS" in command
            or command == "goodbye"
            or command == "quit"
        ):
            print("JARVIS: Goodbye Sam!")
            break


if __name__ == "__main__":
    start_assistant()

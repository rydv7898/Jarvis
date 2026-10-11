
from datetime import datetime
import requests
import webbrowser
import subprocess
import re

from commands.router import route_command
from core.time_parser import parse_time_expression
from core.conversation import get_conversation_response
from ai.gemini_ai import ask_gemini

from music.music import (
    play_favorite_song,
    play_favorite_playlist,
)

from core.reminder import (
    add_reminder,
    list_reminders,
    clear_reminders,
)

from core.tasks import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    clear_tasks,
)

from core.notes import (
    add_note,
    list_notes,
    delete_note,
    clear_notes,
)

from core.system_control import (
    lock_computer,
    open_settings,
    open_task_manager,
    open_control_panel,
    open_file_explorer,
    shutdown_computer,
    restart_computer,
    cancel_shutdown,
)


pending_system_action = None

def process_command(text, history=None):
    global pending_system_action

    original_text = text.strip()
    text = original_text.lower()

    if not text:
        return "Please say a command."

    # ---------------- CONFIRMATION ----------------

    if pending_system_action == "shutdown":
        if text in (
            "yes",
            "yes shutdown",
            "confirm",
            "confirm shutdown",
            "do it",
            "shut down",
        ):
            pending_system_action = None
            return shutdown_computer()

        pending_system_action = None
        return "Shutdown cancelled."

    if pending_system_action == "restart":
        if text in (
            "yes",
            "yes restart",
            "confirm",
            "confirm restart",
            "do it",
            "restart",
        ):
            pending_system_action = None
            return restart_computer()

        pending_system_action = None
        return "Restart cancelled."

    # ---------------- ROUTER ----------------

    command_type = route_command(text)

    # ---------------- BASIC COMMANDS ----------------

    if text in ("hello", "hi", "hey", "hello jarvis", "hi jarvis","good morning", "good afternoon", "good evening","hey hi javis"):
        return "Hello Sam! How can I help you?"

    if "your name" in text:
        return "My name is JARVIS. I am your AI assistant."

    # ---------------- CONVERSATION ----------------

    conversation_response = get_conversation_response(original_text)

    if conversation_response is not None:
        return conversation_response

    # ---------------- TASK MANAGEMENT ----------------

    if command_type == "task":

        if any(phrase in text for phrase in (
            "add a task",
            "add task",
            "create a task",
            "create task",
            "new task",
        )):
            match = re.search(
                r"(?:add a task|add task|create a task|create task|new task)"
                r"\s+(?:to\s+)?(.+)",
                original_text,
                re.IGNORECASE,
            )

            if not match:
                return (
                    "Please tell me the task, for example: "
                    "add a task to study Python."
                )

            title = match.group(1).strip()
            return add_task(title)

        if any(phrase in text for phrase in (
            "show my task",
            "show my tasks",
            "show task",
            "show tasks",
            "list task",
            "list tasks",
            "my task",
            "my tasks",
            "pending task",
            "pending tasks",
        )):
            return list_tasks()

        if (
            "complete task" in text
            or "finish task" in text
            or "mark task" in text
            or ("task" in text and ("done" in text or "completed" in text))
        ):
            match = re.search(
                r"(?:complete task|finish task|mark task|task)"
                r"\s+(\d+)",
                text,
            )

            if not match:
                return "Please tell me the task number, for example: complete task 1."

            return complete_task(int(match.group(1)))

        if "delete task" in text or "remove task" in text:
            match = re.search(
                r"(?:delete task|remove task)\s+(\d+)",
                text,
            )

            if not match:
                return "Please tell me the task number, for example: delete task 1."

            return delete_task(int(match.group(1)))

        if any(phrase in text for phrase in (
            "clear task",
            "clear tasks",
            "delete all task",
            "delete all tasks",
            "remove all task",
            "remove all tasks",
        )):
            return clear_tasks()

    # ---------------- NOTES MANAGEMENT ----------------

    elif command_type == "note":

        if any(phrase in text for phrase in (
            "add a note",
            "add note",
            "take a note",
            "take note",
            "create a note",
            "create note",
            "new note",
        )):
            match = re.search(
                r"(?:add a note|add note|take a note|take note|"
                r"create a note|create note|new note)"
                r"\s+(?:(?:that|to)\s+)?(.+)",
                original_text,
                re.IGNORECASE,
            )

            if not match:
                return "Please tell me the note, for example: add a note to study NumPy."

            return add_note(match.group(1).strip())

        if any(phrase in text for phrase in (
            "show my note",
            "show my notes",
            "show note",
            "show notes",
            "list note",
            "list notes",
            "my note",
            "my notes",
        )):
            return list_notes()

        if "delete note" in text or "remove note" in text:
            match = re.search(
                r"(?:delete note|remove note)\s+(\d+)",
                text,
            )

            if not match:
                return "Please tell me the note number, for example: delete note 1."

            return delete_note(int(match.group(1)))

        if any(phrase in text for phrase in (
            "clear note",
            "clear notes",
            "delete all note",
            "delete all notes",
            "remove all note",
            "remove all notes",
        )):
            return clear_notes()

    # ---------------- REMINDERS ----------------

    elif command_type == "reminder":

        if "remind me" in text or "set a reminder" in text:
            seconds, time_description = parse_time_expression(text)

            if seconds is None:
                return (
                    "Please tell me when to remind you, for example: "
                    "remind me in 10 minutes to study."
                )

            message_match = re.search(
                r"(?:after|in)\s+"
                r"(?:\d+\s+(?:seconds?|minutes?|hours?)|half\s+an?\s+hour)"
                r"\s+(?:to|that)\s+(.+)",
                original_text,
                re.IGNORECASE,
            )

            if message_match:
                message = message_match.group(1).strip()
            else:
                clock_match = re.search(
                    r"\b(?:today|tomorrow)"
                    r"(?:\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm))?"
                    r"\s+(?:to|that)\s+(.+)",
                    original_text,
                    re.IGNORECASE,
                )

                if clock_match:
                    message = clock_match.group(1).strip()
                else:
                    message = "This is your reminder."

            add_reminder(message, seconds)

            return (
                f"Okay Sam, I will remind you in "
                f"{time_description} to {message}."
            )

        if any(phrase in text for phrase in (
            "list reminder",
            "list reminders",
            "show reminder",
            "show reminders",
        )):
            return list_reminders()

        if any(phrase in text for phrase in (
            "clear reminder",
            "clear reminders",
            "delete reminder",
            "delete reminders",
        )):
            return clear_reminders()

    # ---------------- SYSTEM CONTROL ----------------

    elif command_type == "system":

        if any(phrase in text for phrase in (
            "shut down my computer",
            "shutdown my computer",
            "shut down computer",
            "shutdown computer",
            "turn off my computer",
            "turn off computer",
        )):
            pending_system_action = "shutdown"
            return (
                "Are you sure you want to shut down your computer? "
                "Please say yes to confirm."
            )

        if any(phrase in text for phrase in (
            "restart my computer",
            "restart computer",
            "reboot my computer",
            "reboot computer",
        )):
            pending_system_action = "restart"
            return (
                "Are you sure you want to restart your computer? "
                "Please say yes to confirm."
            )

        if "cancel shutdown" in text or "cancel shut down" in text:
            pending_system_action = None
            return cancel_shutdown()

        if any(phrase in text for phrase in (
            "lock my computer",
            "lock computer",
            "lock my pc",
            "lock pc",
        )):
            return lock_computer()

        if "open settings" in text or "open windows settings" in text:
            return open_settings()

        if "open task manager" in text or "open taskmanager" in text:
            return open_task_manager()

        if "open control panel" in text:
            return open_control_panel()

        if "open file explorer" in text or "open explorer" in text:
            return open_file_explorer()

    # ---------------- MUSIC ----------------

    elif command_type == "music":

        if "playlist" in text and (
            "favorite" in text or "favourite" in text
        ):
            return play_favorite_playlist()

        if "song" in text and (
            "favorite" in text or "favourite" in text
        ):
            return play_favorite_song()

        if "music" in text and (
            "favorite" in text or "favourite" in text
        ):
            return play_favorite_playlist()

    # ---------------- WEATHER ----------------

    elif command_type == "weather":

        try:
            url = (
                "https://api.open-meteo.com/v1/forecast"
                "?latitude=18.5204"
                "&longitude=73.8567"
                "&current=temperature_2m"
            )

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            temperature = weather_data["current"]["temperature_2m"]

            return (
                f"The current temperature in Pune is "
                f"{temperature} degrees Celsius."
            )

        except requests.exceptions.RequestException as error:
            print("Weather request error:", repr(error))
            return "Sorry, I could not connect to the weather service."

        except (KeyError, TypeError, ValueError) as error:
            print("Weather data error:", repr(error))
            return "Sorry, I could not get the current temperature."

    # ---------------- TIME / DATE ----------------

    elif command_type == "time_date":

        if "time" in text:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."

        if "date" in text:
            current_date = datetime.now().strftime("%B %d, %Y")
            return f"Today is {current_date}."

        if "day" in text:
            current_day = datetime.now().strftime("%A")
            return f"Today is {current_day}."

    # ---------------- APPLICATIONS ----------------

    elif command_type == "application":

        if "open edge" in text or "open microsoft edge" in text:
            try:
                subprocess.Popen("msedge")
                return "Opening Microsoft Edge."
            except Exception as error:
                print("Edge error:", repr(error))
                return "Sorry, I could not open Microsoft Edge."

        if "open browser" in text:
            webbrowser.open("https://www.google.com")
            return "Opening your web browser."

        if "open vs code" in text or "open visual studio code" in text:
            try:
                subprocess.Popen("code")
                return "Opening Visual Studio Code."
            except Exception as error:
                print("VS Code error:", repr(error))
                return "Sorry, I could not open Visual Studio Code."

        if "open youtube" in text:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."

        if "open chatgpt" in text:
            webbrowser.open("https://chatgpt.com")
            return "Opening ChatGPT."

        if "open github" in text:
            webbrowser.open("https://github.com")
            return "Opening GitHub."

    # ---------------- STOP ----------------

    if text in ("stop", "exit", "quit", "goodbye"):
        return "Goodbye Sam!"

    # ---------------- GEMINI AI FALLBACK ----------------


    # ---------------- AI FALLBACK ----------------

    try:
        print("JARVIS is thinking...")
        answer = ask_gemini(original_text, history=history)

        if answer:
            return answer

        return "Sorry Sam, the AI providers returned an empty response."

    except Exception as error:
        print("JARVIS AI error:", repr(error))
        return (
            "Sorry Sam, I couldn't answer that right now. "
            "Please check the AI connection."
        )

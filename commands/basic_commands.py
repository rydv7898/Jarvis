from datetime import datetime
import requests
import webbrowser
import subprocess
import re

from commands.router import route_command
from core.time_parser import parse_time_expression
from core.conversation import get_conversation_response

from music.music import (
    play_favorite_song,
    play_favorite_playlist
)

from core.reminder import (
    add_reminder,
    list_reminders,
    clear_reminders
)

from core.tasks import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    clear_tasks
)

from core.notes import (
    add_note,
    list_notes,
    delete_note,
    clear_notes
)

from core.system_control import (
    lock_computer,
    open_settings,
    open_task_manager,
    open_control_panel,
    open_file_explorer,
    shutdown_computer,
    restart_computer,
    cancel_shutdown
)


pending_system_action = None


def process_command(text):

    global pending_system_action

    # Keep original user command
    original_text = text.strip()

    # Lowercase version for command detection
    text = original_text.lower()

    # ---------------- CONFIRMATION ----------------

    if pending_system_action == "shutdown":

        if text in (
            "yes",
            "yes shutdown",
            "confirm",
            "confirm shutdown",
            "do it",
            "shut down"
        ):

            pending_system_action = None

            return shutdown_computer()

        else:

            pending_system_action = None

            return "Shutdown cancelled."

    if pending_system_action == "restart":

        if text in (
            "yes",
            "yes restart",
            "confirm",
            "confirm restart",
            "do it",
            "restart"
        ):

            pending_system_action = None

            return restart_computer()

        else:

            pending_system_action = None

            return "Restart cancelled."

    # ---------------- ROUTER ----------------

    command_type = route_command(text)

    # ---------------- BASIC COMMANDS ----------------

    if "hello" in text or "hi" in text:

        return "Hello Sam! How can I help you?"

    elif "your name" in text:

        return (
            "My name is SAMSHIV. "
            "I am your AI assistant."
        )

    # ---------------- CONVERSATION ----------------

    conversation_response = get_conversation_response(
        original_text
    )

    if conversation_response is not None:

        return conversation_response

    # ---------------- TASK MANAGEMENT ----------------

    elif command_type == "task":

        if (
            "add a task" in text
            or "add task" in text
            or "create a task" in text
            or "create task" in text
            or "new task" in text
        ):

            match = re.search(
                r"(?:add a task|add task|create a task|create task|new task)"
                r"\s+(?:to\s+)?(.+)",
                original_text,
                re.IGNORECASE
            )

            if not match:

                return (
                    "Please tell me the task, "
                    "for example: "
                    "add a task to study Python."
                )

            title = match.group(1).strip()

            return add_task(title)

        elif (
            "show my task" in text
            or "show my tasks" in text
            or "show task" in text
            or "show tasks" in text
            or "list task" in text
            or "list tasks" in text
            or "my task" in text
            or "my tasks" in text
            or "pending task" in text
            or "pending tasks" in text
        ):

            return list_tasks()

        elif (
            "complete task" in text
            or "finish task" in text
            or "mark task" in text
            or ("task" in text and "done" in text)
            or ("task" in text and "completed" in text)
        ):

            match = re.search(
                r"(?:complete task|finish task|mark task|task)"
                r"\s*(\d+)",
                text
            )

            if not match:

                return (
                    "Please tell me the task number, "
                    "for example: complete task 1."
                )

            task_id = int(match.group(1))

            return complete_task(task_id)

        elif (
            "delete task" in text
            or "remove task" in text
        ):

            match = re.search(
                r"(?:delete task|remove task)\s+(\d+)",
                text
            )

            if not match:

                return (
                    "Please tell me the task number, "
                    "for example: delete task 1."
                )

            task_id = int(match.group(1))

            return delete_task(task_id)

        elif (
            "clear task" in text
            or "clear tasks" in text
            or "delete all task" in text
            or "delete all tasks" in text
            or "remove all task" in text
            or "remove all tasks" in text
        ):

            return clear_tasks()

    # ---------------- NOTES MANAGEMENT ----------------

    elif command_type == "note":

        if (
            "add a note" in text
            or "add note" in text
            or "take a note" in text
            or "take note" in text
            or "create a note" in text
            or "create note" in text
            or "new note" in text
        ):

            match = re.search(
                r"(?:add a note|add note|take a note|take note|"
                r"create a note|create note|new note)"
                r"\s+(?:that\s+|to\s+)?(.+)",
                original_text,
                re.IGNORECASE
            )

            if not match:

                return (
                    "Please tell me the note, "
                    "for example: "
                    "add a note to study NumPy."
                )

            content = match.group(1).strip()

            return add_note(content)

        elif (
            "show my note" in text
            or "show my notes" in text
            or "show note" in text
            or "show notes" in text
            or "list note" in text
            or "list notes" in text
            or "my note" in text
            or "my notes" in text
        ):

            return list_notes()

        elif (
            "delete note" in text
            or "remove note" in text
        ):

            match = re.search(
                r"(?:delete note|remove note)\s+(\d+)",
                text
            )

            if not match:

                return (
                    "Please tell me the note number, "
                    "for example: delete note 1."
                )

            note_id = int(match.group(1))

            return delete_note(note_id)

        elif (
            "clear note" in text
            or "clear notes" in text
            or "delete all note" in text
            or "delete all notes" in text
            or "remove all note" in text
            or "remove all notes" in text
        ):

            return clear_notes()

    # ---------------- REMINDERS ----------------

    elif command_type == "reminder":

        if (
            "remind me" in text
            or "set a reminder" in text
        ):

            seconds, time_description = (
                parse_time_expression(text)
            )

            if seconds is None:

                return (
                    "Please tell me when to remind you, "
                    "for example: "
                    "remind me in 10 minutes to study."
                )

            # NORMAL RELATIVE TIME

            message_match = re.search(
                r"(?:after|in)\s+"
                r"(?:\d+\s*"
                r"(?:second|seconds|minute|minutes|hour|hours)"
                r"|half\s+an?\s+hour)"
                r"\s+(?:to|that)\s+(.+)",
                original_text,
                re.IGNORECASE
            )

            if message_match:

                message = message_match.group(1).strip()

            else:

                # TODAY / TOMORROW TIME

                clock_match = re.search(
                    r"\b(?:today|tomorrow)"
                    r"(?:\s+at\s+\d{1,2}"
                    r"(?:\:\d{2})?"
                    r"\s*(?:am|pm))?"
                    r"\s+(?:to|that)\s+(.+)",
                    original_text,
                    re.IGNORECASE
                )

                if clock_match:

                    message = clock_match.group(1).strip()

                else:

                    message = "This is your reminder."

            add_reminder(
                message,
                seconds
            )

            return (
                f"Okay Sam, I will remind you "
                f"in {time_description} "
                f"to {message}."
            )

        elif (
            "list reminder" in text
            or "list reminders" in text
            or "show reminder" in text
            or "show reminders" in text
        ):

            return list_reminders()

        elif (
            "clear reminder" in text
            or "clear reminders" in text
            or "delete reminder" in text
            or "delete reminders" in text
        ):

            return clear_reminders()

    # ---------------- SYSTEM CONTROL ----------------

    elif command_type == "system":

        if (
            "shut down my computer" in text
            or "shutdown my computer" in text
            or "shut down computer" in text
            or "shutdown computer" in text
            or "turn off my computer" in text
            or "turn off computer" in text
        ):

            pending_system_action = "shutdown"

            return (
                "Are you sure you want to shut down "
                "your computer? Please say yes to confirm."
            )

        elif (
            "restart my computer" in text
            or "restart computer" in text
            or "reboot my computer" in text
            or "reboot computer" in text
        ):

            pending_system_action = "restart"

            return (
                "Are you sure you want to restart "
                "your computer? Please say yes to confirm."
            )

        elif (
            "cancel shutdown" in text
            or "cancel shut down" in text
        ):

            pending_system_action = None

            return cancel_shutdown()

        elif (
            "lock my computer" in text
            or "lock computer" in text
            or "lock my pc" in text
            or "lock pc" in text
        ):

            return lock_computer()

        elif (
            "open settings" in text
            or "open windows settings" in text
        ):

            return open_settings()

        elif (
            "open task manager" in text
            or "open taskmanager" in text
        ):

            return open_task_manager()

        elif "open control panel" in text:

            return open_control_panel()

        elif (
            "open file explorer" in text
            or "open explorer" in text
        ):

            return open_file_explorer()

    # ---------------- MUSIC ----------------

    elif command_type == "music":

        if "playlist" in text and (
            "favorite" in text
            or "favourite" in text
        ):

            return play_favorite_playlist()

        elif "song" in text and (
            "favorite" in text
            or "favourite" in text
        ):

            return play_favorite_song()

        elif "music" in text and (
            "favorite" in text
            or "favourite" in text
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

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            weather_data = response.json()

            temperature = weather_data[
                "current"
            ][
                "temperature_2m"
            ]

            return (
                f"The current temperature in Pune is "
                f"{temperature} degrees Celsius."
            )

        except requests.exceptions.RequestException:

            return (
                "Sorry, I could not connect "
                "to the weather service."
            )

        except Exception:

            return (
                "Sorry, I could not get "
                "the current temperature."
            )

    # ---------------- TIME / DATE ----------------

    elif command_type == "time_date":

        if "time" in text:

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            return (
                f"The current time is "
                f"{current_time}."
            )

        elif "date" in text:

            current_date = datetime.now().strftime(
                "%B %d, %Y"
            )

            return (
                f"Today is "
                f"{current_date}."
            )

        elif "day" in text:

            current_day = datetime.now().strftime(
                "%A"
            )

            return (
                f"Today is "
                f"{current_day}."
            )

    # ---------------- APPLICATIONS ----------------

    elif command_type == "application":

        if (
            "open edge" in text
            or "open microsoft edge" in text
        ):

            try:

                subprocess.Popen("msedge")

                return "Opening Microsoft Edge."

            except Exception:

                return (
                    "Sorry, I could not open "
                    "Microsoft Edge."
                )

        elif "open browser" in text:

            webbrowser.open(
                "https://www.google.com"
            )

            return "Opening your web browser."

        elif (
            "open vs code" in text
            or "open visual studio code" in text
        ):

            try:

                subprocess.Popen("code")

                return "Opening Visual Studio Code."

            except Exception:

                return (
                    "Sorry, I could not open "
                    "Visual Studio Code."
                )

        elif "open youtube" in text:

            webbrowser.open(
                "https://www.youtube.com"
            )

            return "Opening YouTube."

        elif "open chatgpt" in text:

            webbrowser.open(
                "https://chatgpt.com"
            )

            return "Opening ChatGPT."

        elif "open github" in text:

            webbrowser.open(
                "https://github.com"
            )

            return "Opening GitHub."

    # ---------------- STOP ----------------

    elif (
        "stop" in text
        or "exit" in text
    ):

        return "Goodbye Sam!"

    # ---------------- UNKNOWN ----------------

    return (
        f"Sorry Sam, I don't understand "
        f"the command: {original_text}"
    ) 
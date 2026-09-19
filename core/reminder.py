import threading
import json
import os
from datetime import datetime, timedelta

from voice.text_to_speech import speak


REMINDER_FILE = os.path.join(
    os.path.dirname(__file__),
    "reminders.json"
)


reminders = []


def save_reminders():

    with open(
        REMINDER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            reminders,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_reminders():

    global reminders

    if not os.path.exists(REMINDER_FILE):

        reminders = []

        return

    try:

        with open(
            REMINDER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            reminders = json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        reminders = []


def get_next_reminder_id():

    if not reminders:

        return 1

    return max(
        reminder["id"]
        for reminder in reminders
    ) + 1


def add_reminder(
    message,
    seconds
):

    reminder_id = get_next_reminder_id()

    trigger_time = (
        datetime.now()
        + timedelta(seconds=seconds)
    )

    reminder = {
        "id": reminder_id,
        "message": message,
        "trigger_time": trigger_time.isoformat(),
        "active": True
    }

    reminders.append(reminder)

    save_reminders()

    start_timer(reminder)

    return (
        f"Reminder {reminder_id} set for "
        f"{seconds} seconds from now."
    )


def start_timer(reminder):

    if not reminder["active"]:

        return

    trigger_time = datetime.fromisoformat(
        reminder["trigger_time"]
    )

    remaining_seconds = (
        trigger_time - datetime.now()
    ).total_seconds()

    if remaining_seconds <= 0:

        show_reminder(
            reminder["id"],
            reminder["message"]
        )

        return

    timer = threading.Timer(
        remaining_seconds,
        show_reminder,
        args=[
            reminder["id"],
            reminder["message"]
        ]
    )

    timer.daemon = True

    timer.start()


def show_reminder(
    reminder_id,
    message
):

    reminder_found = False

    for reminder in reminders:

        if reminder["id"] == reminder_id:

            if not reminder["active"]:

                return

            reminder["active"] = False

            reminder_found = True

            break

    if not reminder_found:

        return

    save_reminders()

    print()

    print("🔔 SAMSHIV REMINDER")

    print(
        f"Reminder {reminder_id}: "
        f"{message}"
    )

    print()

    speak(
        f"Sam, this is reminder number "
        f"{reminder_id}. {message}"
    )


def list_reminders():

    load_reminders()

    if not reminders:

        return "You have no reminders."

    print()

    print("📋 SAMSHIV REMINDERS")

    active_count = 0

    for reminder in reminders:

        if reminder["active"]:

            status = "Active"

            active_count += 1

        else:

            status = "Completed"

        trigger_time = datetime.fromisoformat(
            reminder["trigger_time"]
        )

        print(
            f"{reminder['id']}. "
            f"{reminder['message']} "
            f"- "
            f"{trigger_time.strftime('%I:%M:%S %p')} "
            f"- "
            f"{status}"
        )

    return (
        f"You have {len(reminders)} "
        f"reminder(s), with "
        f"{active_count} active."
    )


def clear_reminders():

    global reminders

    for reminder in reminders:

        reminder["active"] = False

    save_reminders()

    return "All reminders have been cleared."


def restore_active_reminders():

    load_reminders()

    for reminder in reminders:

        if reminder["active"]:

            start_timer(reminder)


restore_active_reminders()
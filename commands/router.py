def route_command(text):
    """
    Decide which type of command the user has given.
    """

    text = text.lower().strip()

    # --------------------------------
    # SYSTEM COMMANDS
    # --------------------------------

    # Specific system commands must come
    # before generic "task" detection.

    if (
        "open task manager" in text
        or "open taskmanager" in text
        or "open settings" in text
        or "open windows settings" in text
        or "open control panel" in text
        or "open file explorer" in text
        or "open explorer" in text
        or "lock my computer" in text
        or "lock computer" in text
        or "lock my pc" in text
        or "lock pc" in text
        or "shut down my computer" in text
        or "shutdown my computer" in text
        or "shut down computer" in text
        or "shutdown computer" in text
        or "turn off my computer" in text
        or "turn off computer" in text
        or "restart my computer" in text
        or "restart computer" in text
        or "reboot my computer" in text
        or "reboot computer" in text
        or "cancel shutdown" in text
        or "cancel shut down" in text
    ):

        return "system"

    # --------------------------------
    # APPLICATION COMMANDS
    # --------------------------------

    if (
        "open edge" in text
        or "open microsoft edge" in text
        or "open browser" in text
        or "open youtube" in text
        or "open chatgpt" in text
        or "open github" in text
        or "open vs code" in text
        or "open visual studio code" in text
    ):

        return "application"

    # --------------------------------
    # MUSIC COMMANDS
    # --------------------------------

    if (
        "play" in text
        and (
            "song" in text
            or "music" in text
            or "playlist" in text
        )
    ):

        return "music"

    if (
        "song" in text
        or "playlist" in text
        or "music" in text
    ):

        return "music"

    # --------------------------------
    # REMINDER COMMANDS
    # --------------------------------

    if (
        "remind" in text
        or "reminder" in text
        or "reminders" in text
    ):

        return "reminder"

    # --------------------------------
    # NOTE COMMANDS
    # --------------------------------

    if (
        "note" in text
        or "notes" in text
    ):

        return "note"

    # --------------------------------
    # TASK COMMANDS
    # --------------------------------

    if (
        "task" in text
        or "tasks" in text
    ):

        return "task"

    # --------------------------------
    # WEATHER
    # --------------------------------

    if (
        "weather" in text
        or "temperature" in text
    ):

        return "weather"

    # --------------------------------
    # TIME / DATE
    # --------------------------------

    if (
        "time" in text
        or "date" in text
        or "day" in text
    ):

        return "time_date"

    # --------------------------------
    # UNKNOWN COMMAND
    # --------------------------------

    return "unknown"
import re
from datetime import datetime, timedelta


def parse_time_expression(text):
    """
    Convert a natural reminder time expression
    into the number of seconds from now.

    Returns:
        seconds, description
    """

    text = text.lower().strip()

    # --------------------------------
    # HALF AN HOUR
    # --------------------------------

    if re.search(
        r"\bhalf\s+an?\s+hour\b",
        text
    ):

        return (
            30 * 60,
            "half an hour"
        )

    # --------------------------------
    # NUMBER + UNIT
    # --------------------------------

    match = re.search(
        r"\b(\d+)\s*"
        r"(second|seconds|minute|minutes|hour|hours)\b",
        text
    )

    if match:

        amount = int(
            match.group(1)
        )

        unit = match.group(2)

        if "second" in unit:

            seconds = amount

        elif "minute" in unit:

            seconds = amount * 60

        elif "hour" in unit:

            seconds = amount * 60 * 60

        else:

            return None, None

        return (
            seconds,
            f"{amount} {unit}"
        )

    # --------------------------------
    # TODAY / TOMORROW AT SPECIFIC TIME
    # --------------------------------

    specific_time_match = re.search(
        r"\b(today|tomorrow)\s+at\s+"
        r"(\d{1,2})"
        r"(?:\:(\d{2}))?"
        r"\s*(am|pm)\b",
        text
    )

    if specific_time_match:

        day_name = specific_time_match.group(1)

        hour = int(
            specific_time_match.group(2)
        )

        minute = int(
            specific_time_match.group(3)
            or 0
        )

        period = specific_time_match.group(4)

        # Validate hour

        if hour < 1 or hour > 12:

            return None, None

        # Validate minute

        if minute < 0 or minute > 59:

            return None, None

        # Convert 12-hour format
        # to 24-hour format

        if period == "am":

            if hour == 12:

                hour = 0

        else:

            if hour != 12:

                hour += 12

        now = datetime.now()

        # --------------------------------
        # TODAY
        # --------------------------------

        if day_name == "today":

            target = now.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            # If today's time has already passed,
            # schedule it for tomorrow.

            if target <= now:

                target = target + timedelta(
                    days=1
                )

                description = (
                    f"tomorrow at "
                    f"{specific_time_match.group(2)}"
                    f"{':' + specific_time_match.group(3) if specific_time_match.group(3) else ''}"
                    f" {period.upper()}"
                )

            else:

                description = (
                    f"today at "
                    f"{specific_time_match.group(2)}"
                    f"{':' + specific_time_match.group(3) if specific_time_match.group(3) else ''}"
                    f" {period.upper()}"
                )

        # --------------------------------
        # TOMORROW
        # --------------------------------

        else:

            target = now + timedelta(
                days=1
            )

            target = target.replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            )

            description = (
                f"tomorrow at "
                f"{specific_time_match.group(2)}"
                f"{':' + specific_time_match.group(3) if specific_time_match.group(3) else ''}"
                f" {period.upper()}"
            )

        seconds = (
            target - datetime.now()
        ).total_seconds()

        return (
            int(seconds),
            description
        )

    # --------------------------------
    # TOMORROW
    # --------------------------------

    if re.search(
        r"\btomorrow\b",
        text
    ):

        now = datetime.now()

        target = now + timedelta(
            days=1
        )

        target = target.replace(
            hour=9,
            minute=0,
            second=0,
            microsecond=0
        )

        seconds = (
            target - datetime.now()
        ).total_seconds()

        return (
            int(seconds),
            "tomorrow at 9 AM"
        )

    # --------------------------------
    # UNKNOWN
    # --------------------------------

    return None, None
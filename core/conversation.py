import random


def get_conversation_response(text):
    """
    Handle simple conversational commands.

    Returns:
        A response string if recognized,
        otherwise None.
    """

    text = text.lower().strip()

    # --------------------------------
    # HOW ARE YOU
    # --------------------------------

    if (
        "how are you" in text
        or "how are you doing" in text
    ):

        responses = [
            "I'm doing great, Sam. Thanks for asking!",
            "I'm running perfectly and ready to help you.",
            "I'm doing well, Sam. What are we working on today?"
        ]

        return random.choice(responses)

    # --------------------------------
    # THANK YOU
    # --------------------------------

    if (
        "thank you" in text
        or "thanks" in text
        or "thank u" in text
    ):

        responses = [
            "You're welcome, Sam!",
            "Anytime, Sam!",
            "Glad I could help!"
        ]

        return random.choice(responses)

    # --------------------------------
    # GOOD MORNING
    # --------------------------------

    if "good morning" in text:

        return (
            "Good morning Sam! "
            "Ready to make today productive?"
        )

    # --------------------------------
    # GOOD AFTERNOON
    # --------------------------------

    if "good afternoon" in text:

        return (
            "Good afternoon Sam! "
            "How is your day going?"
        )

    # --------------------------------
    # GOOD EVENING
    # --------------------------------

    if "good evening" in text:

        return (
            "Good evening Sam! "
            "How was your day?"
        )

    # --------------------------------
    # GOOD NIGHT
    # --------------------------------

    if "good night" in text:

        return (
            "Good night Sam! "
            "Have a good rest."
        )

    # --------------------------------
    # WHO ARE YOU
    # --------------------------------

    if (
        "who are you" in text
        or "what are you" in text
    ):

        return (
            "I am SAMSHIV, your personal Python "
            "voice assistant."
        )

    # --------------------------------
    # WHAT CAN YOU DO
    # --------------------------------

    if (
        "what can you do" in text
        or "what do you do" in text
        or "your capabilities" in text
    ):

        return (
            "I can manage tasks and notes, "
            "create reminders, play music, "
            "check the weather, open applications, "
            "control some computer functions, "
            "and have simple conversations."
        )

    # --------------------------------
    # WHAT ARE YOU DOING
    # --------------------------------

    if "what are you doing" in text:

        return (
            "I'm here waiting for your next command, Sam."
        )

    # --------------------------------
    # BORED
    # --------------------------------

    if (
        "i am bored" in text
        or "i'm bored" in text
        or "im bored" in text
    ):

        return (
            "Let's do something productive. "
            "We could study Python, work on SAMSHIV, "
            "or practice English."
        )

    # --------------------------------
    # TIRED
    # --------------------------------

    if (
        "i am tired" in text
        or "i'm tired" in text
        or "im tired" in text
    ):

        return (
            "You should take a short break, Sam. "
            "A little rest can help you come back "
            "with more focus."
        )

    # --------------------------------
    # MOTIVATION
    # --------------------------------

    if (
        "motivate me" in text
        or "give me motivation" in text
    ):

        responses = [
            "Small progress every day becomes massive progress over time.",
            "You don't need to be perfect. You just need to keep moving.",
            "Focus on today's work. Let tomorrow take care of itself.",
            "Your future skills are built by what you practice today."
        ]

        return random.choice(responses)

    # --------------------------------
    # UNKNOWN CONVERSATION
    # --------------------------------

    return None
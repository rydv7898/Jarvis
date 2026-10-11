import json
import os


NOTE_FILE = os.path.join(
    os.path.dirname(__file__),
    "notes.json"
)


notes = []


def save_notes():
    with open(
        NOTE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            notes,
            file,
            indent=4
        )


def load_notes():

    global notes

    if not os.path.exists(NOTE_FILE):
        notes = []
        return

    try:

        with open(
            NOTE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            notes = json.load(file)

    except (json.JSONDecodeError, OSError):

        notes = []


def get_next_note_id():

    if not notes:
        return 1

    return max(
        note["id"]
        for note in notes
    ) + 1


def add_note(content):

    note_id = get_next_note_id()

    note = {
        "id": note_id,
        "content": content
    }

    notes.append(note)

    save_notes()

    return (
        f"Note {note_id} added: {content}"
    )


def list_notes():

    load_notes()

    if not notes:
        return "You have no notes."

    print()
    print("📝 SAMSHIV NOTES")

    for note in notes:

        print(
            f"{note['id']}. "
            f"{note['content']}"
        )

    return (
        f"You have {len(notes)} note(s)."
    )


def delete_note(note_id):

    load_notes()

    for note in notes:

        if note["id"] == note_id:

            notes.remove(note)

            save_notes()

            return (
                f"Note {note_id} deleted."
            )

    return (
        f"Note {note_id} was not found."
    )


def clear_notes():

    global notes

    notes.clear()

    save_notes()

    return "All notes have been cleared."


load_notes()
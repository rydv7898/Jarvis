import json
import os


TASK_FILE = os.path.join(
    os.path.dirname(__file__),
    "tasks.json"
)


tasks = []


def save_tasks():

    with open(
        TASK_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tasks,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_tasks():

    global tasks

    if not os.path.exists(TASK_FILE):
        tasks = []
        return

    try:

        with open(
            TASK_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            tasks = json.load(file)

    except (json.JSONDecodeError, OSError):

        tasks = []


def get_next_task_id():

    if not tasks:
        return 1

    return max(
        task["id"]
        for task in tasks
    ) + 1


def add_task(title):

    task_id = get_next_task_id()

    task = {
        "id": task_id,
        "title": title,
        "completed": False
    }

    tasks.append(task)

    save_tasks()

    return (
        f"Task {task_id} added: {title}"
    )


def list_tasks():

    load_tasks()

    if not tasks:
        return "You have no tasks."

    print()
    print("📋 JARVIS TASKS")

    for task in tasks:

        if task["completed"]:
            status = "Completed"
        else:
            status = "Pending"

        print(
            f"{task['id']}. "
            f"{task['title']} - {status}"
        )

    pending = sum(
        1
        for task in tasks
        if not task["completed"]
    )

    return (
        f"You have {len(tasks)} task(s), "
        f"with {pending} pending."
    )


def complete_task(task_id):

    load_tasks()

    for task in tasks:

        if task["id"] == task_id:

            if task["completed"]:
                return (
                    f"Task {task_id} is already completed."
                )

            task["completed"] = True

            save_tasks()

            return (
                f"Task {task_id} marked as completed."
            )

    return (
        f"Task {task_id} was not found."
    )


def delete_task(task_id):

    load_tasks()

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)

            save_tasks()

            return (
                f"Task {task_id} deleted."
            )

    return (
        f"Task {task_id} was not found."
    )


def clear_tasks():

    global tasks

    tasks.clear()

    save_tasks()

    return "All tasks have been cleared."


load_tasks()

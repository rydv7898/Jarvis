import subprocess


def lock_computer():

    try:

        subprocess.run(
            ["rundll32.exe", "user32.dll,LockWorkStation"],
            check=True
        )

        return "Locking your computer."

    except Exception:

        return "Sorry, I could not lock the computer."


def open_settings():

    try:

        subprocess.Popen(
            "start ms-settings:",
            shell=True
        )

        return "Opening Windows Settings."

    except Exception:

        return "Sorry, I could not open Windows Settings."


def open_task_manager():

    try:

        subprocess.Popen(
            "taskmgr.exe"
        )

        return "Opening Task Manager."

    except Exception:

        return "Sorry, I could not open Task Manager."


def open_control_panel():

    try:

        subprocess.Popen(
            "control.exe"
        )

        return "Opening Control Panel."

    except Exception:

        return "Sorry, I could not open Control Panel."


def open_file_explorer():

    try:

        subprocess.Popen(
            "explorer.exe"
        )

        return "Opening File Explorer."

    except Exception:

        return "Sorry, I could not open File Explorer."


def shutdown_computer():

    try:

        subprocess.Popen(
            ["shutdown", "/s", "/t", "30"]
        )

        return (
            "The computer will shut down "
            "in 30 seconds."
        )

    except Exception:

        return "Sorry, I could not start the shutdown."


def restart_computer():

    try:

        subprocess.Popen(
            ["shutdown", "/r", "/t", "30"]
        )

        return (
            "The computer will restart "
            "in 30 seconds."
        )

    except Exception:

        return "Sorry, I could not start the restart."


def cancel_shutdown():

    try:

        subprocess.Popen(
            ["shutdown", "/a"]
        )

        return "The scheduled shutdown has been cancelled."

    except Exception:

        return "Sorry, I could not cancel the shutdown."
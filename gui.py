
import threading
from datetime import datetime
import tkinter.messagebox as messagebox

import customtkinter as ctk

from commands.basic_commands import process_command
from core.memory import ConversationMemory
from voice.assistant_voice import listen_for_command
from voice.text_to_speech import speak


# ---------------- APPEARANCE ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#071426"
PANEL = "#0D1B30"
CARD = "#10213A"
CYAN = "#00D9FF"
WHITE = "#F4F7FF"
MUTED = "#9DB4D7"
GREEN = "#20D997"
ORANGE = "#FFB454"
RED = "#FF647C"


# ---------------- STARTUP GREETING ----------------

def get_startup_greeting():
    """Choose a greeting based on the computer's local time."""
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning! JARVIS is ready. How can I help?"
    elif 12 <= hour < 17:
        return "Good afternoon! JARVIS is ready. How can I help?"
    elif 17 <= hour < 21:
        return "Good evening! JARVIS is ready. How can I help?"
    return "Hello! JARVIS is ready. How can I help?"


class JARVISApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("JARVIS | AI Voice Assistant")
        self.geometry("1100x720")
        self.minsize(780, 560)
        self.configure(fg_color=BG)

        self.memory = ConversationMemory(max_messages=10)

        self.busy = False
        self.closing = False

        # Continuous listening state.
        # The wake-word detector is not yet connected.
        self.continuous_listening = False
        self.voice_thread = None

        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.build_interface()

        greeting = get_startup_greeting()
        self.add_message("JARVIS", greeting)
        self.set_status("Ready", GREEN)

        # Speak after the window has appeared.
        self.after(700, lambda: self.speak_in_background(greeting))

    # ---------------- INTERFACE ----------------

    def build_interface(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(
            self,
            width=205,
            corner_radius=0,
            fg_color=PANEL
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="🤖 JARVIS",
            font=("Segoe UI", 24, "bold"),
            text_color=CYAN
        ).pack(padx=18, pady=(28, 4), anchor="w")

        ctk.CTkLabel(
            sidebar,
            text="YOUR PERSONAL AI",
            font=("Segoe UI", 10),
            text_color=MUTED
        ).pack(padx=20, pady=(0, 30), anchor="w")

        for item in (
            "⌂   Home",
            "✓   Tasks",
            "▤   Notes",
            "♧   Reminders",
            "♫   Music",
            "☼   Weather",
            "⚙   Settings"
        ):
            ctk.CTkButton(
                sidebar,
                text=item,
                anchor="w",
                height=42,
                fg_color="transparent",
                hover_color=CARD,
                text_color=WHITE,
                command=lambda name=item: self.sidebar_action(name)
            ).pack(fill="x", padx=12, pady=3)

        ctk.CTkLabel(
            sidebar,
            text="Better ideas.\nMore productivity.\nTogether.",
            justify="left",
            text_color=MUTED,
            font=("Segoe UI", 12)
        ).pack(side="bottom", padx=20, pady=24, anchor="w")

        # Main area
        main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew", padx=22, pady=20)

        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            main,
            text="Hello Sam!",
            font=("Segoe UI", 30, "bold"),
            text_color=WHITE
        ).grid(row=0, column=0, sticky="w", pady=(5, 0))

        ctk.CTkLabel(
            main,
            text="I'm JARVIS, your AI voice assistant.",
            font=("Segoe UI", 14),
            text_color=MUTED
        ).grid(row=1, column=0, sticky="w", pady=(4, 15))

        # Chat history
        self.chat = ctk.CTkTextbox(
            main,
            wrap="word",
            font=("Segoe UI", 13),
            fg_color=PANEL,
            text_color=WHITE,
            corner_radius=14,
            border_width=1,
            border_color="#203B5D"
        )
        self.chat.grid(
            row=2, column=0, sticky="nsew", pady=(0, 14)
        )
        self.chat.configure(state="disabled")

        # Status
        self.status = ctk.CTkLabel(
            main,
            text="●  Ready",
            text_color=GREEN,
            font=("Segoe UI", 12, "bold")
        )
        self.status.grid(row=3, column=0, sticky="w", pady=(0, 8))

        # Input controls
        input_frame = ctk.CTkFrame(
            main, fg_color=PANEL, corner_radius=14
        )
        input_frame.grid(
            row=4, column=0, sticky="ew", pady=(0, 8)
        )
        input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type a command or ask a question...",
            height=46,
            font=("Segoe UI", 13),
            fg_color=CARD,
            border_color="#29476B"
        )
        self.entry.grid(
            row=0, column=0, sticky="ew",
            padx=(10, 6), pady=10
        )
        self.entry.bind("<Return>", self.send_command)

        self.mic_button = ctk.CTkButton(
            input_frame,
            text="🎙 Speak",
            width=95,
            height=46,
            fg_color="#173C66",
            hover_color="#205A8C",
            command=self.start_listening
        )
        self.mic_button.grid(row=0, column=1, padx=5, pady=10)

        self.send_button = ctk.CTkButton(
            input_frame,
            text="Send ➤",
            width=90,
            height=46,
            fg_color="#087CF0",
            hover_color="#0865C2",
            command=self.send_command
        )
        self.send_button.grid(
            row=0, column=2, padx=(5, 10), pady=10
        )

        # Stop button for the continuous-listening mode.
        self.stop_button = ctk.CTkButton(
            input_frame,
            text="Stop Listening",
            width=125,
            height=46,
            fg_color="#6E2635",
            hover_color="#963247",
            command=self.stop_continuous_listening,
            state="disabled"
        )
        self.stop_button.grid(row=0, column=3, padx=(0, 10), pady=10)

        ctk.CTkLabel(
            main,
            text=(
                'Try: "What is ESP32?"  •  "Open YouTube"  •  '
                '"Help me study"'
            ),
            text_color=MUTED,
            font=("Segoe UI", 10)
        ).grid(row=5, column=0, sticky="w")

    # ---------------- CHAT HELPERS ----------------

    def add_message(self, sender, text):
        if self.closing:
            return

        self.chat.configure(state="normal")
        self.chat.insert("end", f"{sender}\n{text}\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def set_status(self, text, color=GREEN):
        if not self.closing:
            self.status.configure(
                text=f"●  {text}",
                text_color=color
            )

    def set_busy_controls(self, busy):
        if self.closing:
            return

        self.send_button.configure(
            state="disabled" if busy else "normal"
        )
        self.mic_button.configure(
            state="disabled" if busy else "normal"
        )

    # ---------------- SPEECH OUTPUT ----------------

    def speak_in_background(self, text):
        """Run text-to-speech outside the GUI thread."""
        if self.closing:
            return

        threading.Thread(
            target=self.speak_safely,
            args=(text,),
            daemon=True
        ).start()

    @staticmethod
    def speak_safely(text):
        try:
            speak(text)
        except Exception as error:
            print("Speech output error:", repr(error))

    # ---------------- TEXT COMMANDS ----------------

    def send_command(self, event=None):
        if self.busy or self.closing:
            return

        command = self.entry.get().strip()
        if not command:
            return

        self.entry.delete(0, "end")
        self.add_message("YOU", command)

        normalized = command.lower().strip()

        if normalized in ("exit", "quit", "close window"):
            self.close_app()
            return

        if normalized == "stop listening":
            self.stop_continuous_listening()
            return

        self.start_processing(command)

    # ---------------- AI PROCESSING ----------------

    def start_processing(self, command):
        if self.busy or self.closing:
            return

        self.busy = True
        self.set_status("Processing your request...", CYAN)
        self.set_busy_controls(True)

        threading.Thread(
            target=self.process_in_background,
            args=(command,),
            daemon=True
        ).start()

    def process_in_background(self, command):
        try:
            history = self.memory.get_history()

            response = process_command(
                command,
                history=history
            )
            response = str(
                response or "I couldn't generate a response."
            )

            self.memory.add_message("user", command)
            self.memory.add_message("assistant", response)

            self.after(
                0,
                lambda answer=response: self.show_response(answer)
            )

            self.speak_safely(response)

        except Exception as error:
            print("JARVIS processing error:", repr(error))

            self.after(
                0,
                lambda: self.show_response(
                    "Sorry, an error occurred. "
                    "Check the VS Code terminal for details."
                )
            )

    def show_response(self, response):
        if self.closing:
            return

        self.add_message("JARVIS", response)
        self.busy = False
        self.set_status("Ready", GREEN)
        self.set_busy_controls(False)
        self.entry.focus_set()

    # ---------------- MICROPHONE ----------------

    def start_listening(self):
        if self.busy or self.closing:
            return

        self.busy = True
        self.set_status("Listening for your command...", CYAN)
        self.set_busy_controls(True)

        self.voice_thread = threading.Thread(
            target=self.listen_in_background,
            daemon=True
        )
        self.voice_thread.start()

    def listen_in_background(self):
        try:
            # Uses the existing microphone function.
            text = listen_for_command()

            if self.closing:
                return

            if text:
                self.after(
                    0,
                    lambda command=text: self.handle_voice_command(command)
                )
            else:
                self.after(0, self.voice_not_recognized)

        except Exception as error:
            print("Microphone error:", repr(error))

            if not self.closing:
                self.after(0, self.voice_not_recognized)

    def handle_voice_command(self, command):
        if self.closing:
            return

        self.busy = False
        self.set_busy_controls(False)

        command = command.strip()
        if not command:
            self.voice_not_recognized()
            return

        self.add_message("YOU (VOICE)", command)

        normalized = command.lower().strip()

        if normalized in ("exit", "quit", "close window"):
            self.close_app()
            return

        if normalized == "stop listening":
            self.stop_continuous_listening()
            return

        self.start_processing(command)

    def voice_not_recognized(self):
        if self.closing:
            return

        self.set_status(
            "Couldn't recognize speech. Try again.",
            ORANGE
        )
        self.busy = False
        self.set_busy_controls(False)

    # ---------------- CONTINUOUS LISTENING CONTROL ----------------

    def start_continuous_listening(self):
        """
        Enable the continuous command mode.

        This currently repeats the existing one-command listener.
        It does NOT detect 'Hello JARVIS' while idle.
        """
        if self.closing or self.continuous_listening:
            return

        self.continuous_listening = True
        self.stop_button.configure(state="normal")
        self.set_status(
            'Continuous mode enabled. Say "stop listening" to stop.',
            CYAN
        )

        self.continuous_thread = threading.Thread(
            target=self.continuous_listen_loop,
            daemon=True
        )
        self.continuous_thread.start()

    def continuous_listen_loop(self):
        """
        Repeatedly capture commands using the existing listener.
        Only one listener runs at a time.
        """
        while self.continuous_listening and not self.closing:
            try:
                text = listen_for_command()
            except Exception as error:
                print("Continuous microphone error:", repr(error))
                text = None

            if not self.continuous_listening or self.closing:
                break

            if not text:
                continue

            command = text.strip()
            normalized = command.lower()

            if normalized == "stop listening":
                self.after(0, self.stop_continuous_listening)
                break

            # Wait for the current request to finish before listening again.
            finished = threading.Event()

            def handle_and_signal(command=command):
                try:
                    if self.closing or not self.continuous_listening:
                        return
                    self.add_message("YOU (VOICE)", command)
                    self.start_processing(command)
                finally:
                    finished.set()

            self.after(0, handle_and_signal)

            # Wait for GUI callback to start before checking busy state.
            finished.wait()

            while self.busy and self.continuous_listening and not self.closing:
                threading.Event().wait(0.1)

        if not self.closing:
            self.after(0, self.continuous_loop_finished)

    def stop_continuous_listening(self):
        self.continuous_listening = False

        if self.closing:
            return

        self.stop_button.configure(state="disabled")
        self.set_status("Listening stopped", GREEN)

    def continuous_loop_finished(self):
        if self.closing:
            return

        self.stop_button.configure(state="disabled")
        if not self.busy:
            self.set_status("Ready", GREEN)

    # ---------------- SIDEBAR ----------------

    def sidebar_action(self, name):
        if name.endswith("Home"):
            self.set_status("Home", GREEN)
            return

        suggestions = {
            "✓   Tasks": "Show my tasks",
            "▤   Notes": "Show my notes",
            "♧   Reminders": "Show my reminders",
            "♫   Music": "Play my favourite music",
            "☼   Weather": "Show the weather",
            "⚙   Settings": "Help me with SAMSHIV settings"
        }

        command = suggestions.get(name)
        if command:
            self.entry.delete(0, "end")
            self.entry.insert(0, command)
            self.send_command()

    # ---------------- CLOSE ----------------

    def close_app(self):
        if self.closing:
            return

        self.closing = True
        self.continuous_listening = False

        try:
            self.destroy()
        except Exception as error:
            print("Window shutdown error:", repr(error))


if __name__ == "__main__":
    app = JARVISApp()
    app.mainloop()
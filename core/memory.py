
from collections import deque


class ConversationMemory:
    """Store recent user questions and assistant answers."""

    def __init__(self, max_messages=10):
        self.history = deque(maxlen=max_messages)

    def add_message(self, role, content):
        """Save one message."""
        self.history.append({
            "role": role,
            "content": content
        })

    def get_history(self):
        """Return the saved conversation."""
        return list(self.history)

    def clear(self):
        """Delete conversation history."""
        self.history.clear()
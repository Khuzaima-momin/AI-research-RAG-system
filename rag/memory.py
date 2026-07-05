"""
Enterprise Conversation Memory
==============================

Handles conversation history for the AI Research Assistant.

Features
--------
✓ Conversation memory
✓ Session history
✓ Maximum history length
✓ Context formatting
✓ Clear memory
✓ Future-ready for Redis / Database

Author:
Khuzaima Momin
"""

from collections import deque


# ==========================================================
# CONFIGURATION
# ==========================================================

MAX_HISTORY = 10


# ==========================================================
# Conversation Memory
# ==========================================================

class ConversationMemory:
    """
    Stores conversation history.

    History Format

    User:
        ...

    Assistant:
        ...
    """

    def __init__(self, max_history=MAX_HISTORY):

        self.history = deque(maxlen=max_history)

    # ------------------------------------------------------
    # Add User Message
    # ------------------------------------------------------
    def add_user_message(self, message):

        self.history.append({

            "role": "user",

            "content": message

        })

    # ------------------------------------------------------
    # Add Assistant Message
    # ------------------------------------------------------
    def add_ai_message(self, message):

        self.history.append({

            "role": "assistant",

            "content": message

        })

    # ------------------------------------------------------
    # Return Raw History
    # ------------------------------------------------------
    def get_history(self):

        return list(self.history)

    # ------------------------------------------------------
    # Format History for Gemini
    # ------------------------------------------------------
    def build_history(self):

        if not self.history:
            return ""

        conversation = []

        for msg in self.history:

            if msg["role"] == "user":

                conversation.append(

                    f"User: {msg['content']}"

                )

            else:

                conversation.append(

                    f"Assistant: {msg['content']}"

                )

        return "\n".join(conversation)

    # ------------------------------------------------------
    # Clear Memory
    # ------------------------------------------------------
    def clear(self):

        self.history.clear()

    # ------------------------------------------------------
    # Count Messages
    # ------------------------------------------------------
    def size(self):

        return len(self.history)


# ==========================================================
# Global Memory Instance
# ==========================================================

memory = ConversationMemory()
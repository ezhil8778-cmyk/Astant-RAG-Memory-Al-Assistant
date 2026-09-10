"""
memory.py
Per-session conversation memory, stored as a JSON file so context
persists across turns within a session.
"""

import json
import os


class SessionMemory:
    def __init__(self, session_id, memory_dir="sessions"):
        self.session_id = session_id
        self.memory_dir = memory_dir
        os.makedirs(memory_dir, exist_ok=True)
        self.filepath = os.path.join(memory_dir, f"{session_id}.json")
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)

    def add_turn(self, question, answer):
        self.history.append({"question": question, "answer": answer})
        self._save()

    def recent_turns(self, n=3):
        """Returns the last n question-answer pairs for context."""
        return self.history[-n:]

    def clear(self):
        self.history = []
        self._save()

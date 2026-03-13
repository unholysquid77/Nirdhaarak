from config import MEMORY_WINDOW
from utils.logger import log


class Memory:

    def __init__(self):

        self.history = []

    def add_user(self, text):

        self.history.append({
            "role": "user",
            "content": text
        })

    def add_assistant(self, text):

        self.history.append({
            "role": "assistant",
            "content": text
        })

    def retrieve(self):

        window = self.history[-MEMORY_WINDOW:]

        log(f"Memory retrieved: {len(window)} messages")

        return window

    def clear(self):

        log("Memory cleared")

        self.history = []
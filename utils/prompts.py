from utils.logger import log


class PromptBuilder:

    def __init__(self):

        self.system_blocks = []

        self.context_blocks = []

    def add_system(self, text):

        self.system_blocks.append(text)

    def add_context(self, text):

        self.context_blocks.append(text)

    def build(self, memory, user_input):

        system_prompt = "\n".join(self.system_blocks)

        context = "\n".join(self.context_blocks)

        messages = []

        messages.append({
            "role": "system",
            "content": system_prompt
        })

        if context:

            messages.append({
                "role": "system",
                "content": f"Context:\n{context}"
            })

        messages.extend(memory)

        messages.append({
            "role": "user",
            "content": user_input
        })

        log("Prompt constructed")

        return messages
from utils.prompts import PromptBuilder
from utils.logger import log


class BasicChatPipeline:

    def __init__(self, llm, memory):

        self.llm = llm
        self.memory = memory

        self.personality = "You are an intelligent helpful AI assistant."

    def run(self, user_input):

        log("Running BASIC pipeline")

        builder = PromptBuilder()

        builder.add_system(self.personality)

        history = self.memory.retrieve()

        messages = builder.build(history, user_input)

        response = self.llm.generate(messages)

        self.memory.add_user(user_input)
        self.memory.add_assistant(response)

        return response
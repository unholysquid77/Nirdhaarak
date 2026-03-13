from utils.prompts import PromptBuilder
from utils.logger import log
from modules.rag import RAG


class RAGChatPipeline:

    def __init__(self, llm, memory):

        self.llm = llm
        self.memory = memory

        self.rag = RAG()

        self.system_prompt = """
You are a knowledge grounded assistant.
Use the provided context when answering.
If the context is insufficient, reason carefully.
"""

    def run(self, user_input):

        log("Running RAG pipeline")

        context = self.rag.search(user_input)

        builder = PromptBuilder()

        builder.add_system(self.system_prompt)

        if context:
            builder.add_context("\n".join(context))

        history = self.memory.retrieve()

        messages = builder.build(history, user_input)

        response = self.llm.generate(messages)

        self.memory.add_user(user_input)
        self.memory.add_assistant(response)

        return response
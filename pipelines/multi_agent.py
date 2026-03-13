from utils.prompts import PromptBuilder
from utils.logger import log


class MultiAgentPipeline:

    def __init__(self, llm, memory):

        self.llm = llm
        self.memory = memory

    def agent_a(self, question):

        messages = [
            {"role": "system", "content": "You are an optimistic problem solver."},
            {"role": "user", "content": question}
        ]

        return self.llm.generate(messages)

    def agent_b(self, question):

        messages = [
            {"role": "system", "content": "You are a critical analyst who challenges ideas."},
            {"role": "user", "content": question}
        ]

        return self.llm.generate(messages)

    def judge(self, question, a, b):

        messages = [
            {
                "role": "system",
                "content": "Combine both perspectives into a balanced answer."
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

Answer A:
{a}

Answer B:
{b}

Produce the best final answer.
"""
            }
        ]

        return self.llm.generate(messages)

    def run(self, user_input):

        log("Running MULTI-AGENT pipeline")

        a = self.agent_a(user_input)

        b = self.agent_b(user_input)

        final = self.judge(user_input, a, b)

        self.memory.add_user(user_input)
        self.memory.add_assistant(final)

        return final
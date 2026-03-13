from utils.logger import log


class Router:

    def __init__(self, llm):

        self.llm = llm

        self.routes = {
            "chat": "basic",
            "knowledge": "rag",
            "analysis": "multi_agent"
        }

    def classify_intent(self, user_input):

        prompt = [
            {
                "role": "system",
                "content": "Classify the user's intent into: chat, knowledge, analysis"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        result = self.llm.generate(prompt)

        intent = result.strip().lower()

        log(f"Intent detected: {intent}")

        return intent

    def route(self, user_input):

        intent = self.classify_intent(user_input)

        pipeline = self.routes.get(intent, "basic")

        log(f"Routing to pipeline: {pipeline}")

        return pipeline
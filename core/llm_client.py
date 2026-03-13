from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, MAX_TOKENS
from utils.logger import log
import time


class LLMClient:

    def __init__(self, model=MODEL, max_retries=3):

        self.client = OpenAI(api_key=OPENAI_API_KEY)

        self.model = model

        self.max_retries = max_retries

    def generate(self, messages, temperature=0.7):

        for attempt in range(self.max_retries):

            try:

                log(f"LLM request | model={self.model}")

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=MAX_TOKENS
                )

                output = response.choices[0].message.content

                log("LLM response received")

                return output

            except Exception as e:

                log(f"LLM failure attempt {attempt+1}: {e}")

                time.sleep(1)

        raise RuntimeError("LLM failed after retries")
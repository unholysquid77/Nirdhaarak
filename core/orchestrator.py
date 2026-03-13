from core.llm_client import LLMClient
from modules.memory import Memory
from pipelines.basic_chat import BasicChatPipeline
from core.grade_predictor import predict_grade


class Orchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.memory = Memory()
        self.chat_pipeline = BasicChatPipeline(self.llm, self.memory)
        self.last_prediction = None

    def run(self, user_input):
        text = user_input.lower().strip()

        if text in ["clear", "reset", "exit context"]:
            self.last_prediction = None
            return "SYSTEM: Prediction context cleared. Returning to standard chat."

        if "predict grade" in text:
            return self.run_grade_prediction()

        if self.last_prediction:
            return self.followup_question(user_input)

        return self.chat_pipeline.run(user_input)

    def followup_question(self, question):
        prediction = self.last_prediction["prediction"]
        data = self.last_prediction["student_data"]

        prompt = f"""
        System: A machine learning model predicted the student's grade as: {prediction}.
        Student Feature Matrix: {data}

        User Question: {question}

        Answer based strictly on the prediction and the provided feature matrix. Keep it crisp.
        """
        return self.llm.generate([{"role": "user", "content": prompt}])

    def run_grade_prediction(self, student_data=None):
        if student_data and len(student_data) != 15:
            return "ERR: Invalid input matrix. Expected 15 dimensions."

        if not student_data:
            return "ERR: Execution failed. No student feature matrix provided."

        prediction = predict_grade(student_data)

        self.last_prediction = {
            "prediction": prediction,
            "student_data": student_data
        }
        explanation_prompt = f"""
        You are an AI academic advisor.
        Predicted Grade Category: {prediction}
        Student Feature Matrix (StudyHrs, Attend, ... Stress): {student_data}

        Explain this prediction clearly.
        1. Prediction Summary.
        2. Key Factors (Analyze the specific metrics provided in the matrix).
        3. Interpretation.
        4. Actionable Advice.

        Format beautifully. Be concise.
        """

        explanation = self.llm.generate([{"role": "user", "content": explanation_prompt}])

        return f"Prediction: {prediction}\n\n{explanation}"

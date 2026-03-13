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

    def followup_question(self, question):

        prediction = self.last_prediction["prediction"]

        prompt = f"""
    A student prediction model classified a student as:

    {prediction}

    The user asked a follow-up question about this prediction.

    User Question:
    {question}

    Answer based on the prediction context.
    """

        response = self.llm.generate([
            {"role": "user", "content": prompt}
        ])

        return response
    def run(self, user_input):

        text = user_input.lower()

        if "predict grade" in text:
            return self.run_grade_prediction()

        if self.last_prediction:
            return self.followup_question(user_input)

        return self.chat_pipeline.run(user_input)

    def run_grade_prediction(self, student_data=None):

        example_student = [
            20,  # StudyHours
            85,  # Attendance
            1,   # Resources
            0,   # Extracurricular
            2,   # Motivation
            1,   # Internet
            0,   # Gender
            19,  # Age
            2,   # LearningStyle
            3,   # OnlineCourses
            1,   # Discussions
            80,  # AssignmentCompletion
            90,  # ExamScore
            1,   # EduTech
            1    # StressLevel
        ]

        if student_data and len(student_data) != 15:
            print("Expected 15 features for prediction.")
            return "Error in input. Ask user to recheck and try again."
        if not student_data or student_data == []:
            prediction = predict_grade(example_student)
        else:
            prediction = predict_grade(student_data)
        self.last_prediction = {
            "prediction": prediction,
            "student_data": student_data if student_data else example_student
        }
        explanation_prompt = f"""
        You are an AI academic advisor.

        A machine learning model predicted the student's grade category as:

        {prediction}

        Explain the prediction clearly using the following structure.

        1. **Prediction Summary**
        Briefly explain what this grade category means.

        2. **Key Factors**
        Explain how these factors influence the prediction:
        - Study Hours
        - Attendance
        - Exam Score
        - Assignment Completion
        - Stress Level

        3. **Interpretation**
        What this suggests about the student's academic habits.

        4. **Advice**
        One or two short suggestions that could help the student improve or maintain performance.

        Keep the explanation concise and easy to understand.
        """

        explanation = self.llm.generate([
            {"role": "user", "content": explanation_prompt}
        ])

        return f"""
Prediction: {prediction}

AI Explanation:
{explanation}
"""
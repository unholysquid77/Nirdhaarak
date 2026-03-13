# AI Academic Performance Advisor

An AI-powered system that predicts student academic performance and provides interpretable explanations using machine learning and natural language generation.

Developed for **IEEE CIS – AI Model Quest 2.0**.

---

## Overview

Student academic outcomes are influenced by multiple behavioral and academic factors such as study hours, attendance, exam performance, and stress levels.

This project builds an intelligent system capable of:

- Predicting a student's **Final Grade category**
- Identifying the **key factors affecting performance**
- Providing **AI-generated explanations and insights**
- Allowing users to interact with the system through a chat interface

The system combines **machine learning prediction with a conversational AI interface**, creating a simple academic advisory tool.

---

## Problem Statement

Predict a student's **Final Grade category (0–3)** based on behavioral, psychological, and academic indicators.

Grade Categories:

| Class | Interpretation |
|------|---------------|
| 0 | Highest Performer |
| 1 | Above Average |
| 2 | Below Average |
| 3 | At Risk |

The goal is to enable early identification of students who may need academic support.

---

## Dataset

The dataset contains approximately **14,000 student records** with 15 input features.

Example features include:

- StudyHours
- Attendance
- AssignmentCompletion
- ExamScore
- StressLevel
- LearningStyle
- OnlineCourses
- Motivation
- Internet Access

Target Variable:

Final Grade


---

## Model Approach

We trained a **Random Forest Classifier** to predict student grade categories.

Why Random Forest?

- Works well with tabular datasets
- Handles mixed feature types
- Reduces overfitting through ensemble learning
- Provides feature importance for interpretability

Training Steps:

1. Load dataset
2. Split data into training and testing sets
3. Train Random Forest model
4. Evaluate accuracy and cross-validation
5. Save trained model

---

## Key Insights

Feature importance analysis showed the strongest predictors of academic performance were:

1. ExamScore
2. AssignmentCompletion
3. Attendance
4. StudyHours
5. OnlineCourses

This suggests that **exam performance and academic engagement strongly influence final grade outcomes**.

---

## System Architecture

The project integrates machine learning prediction with an AI explanation layer.

Student Input
↓
ML Prediction Model (Random Forest)
↓
Grade Classification
↓
AI Explanation System
↓
Interactive Chat Interface

Components include:

- ML Prediction Engine
- AI Explanation Layer
- Interactive Chat Interface
- PyQt GUI Dashboard

---

## Demo Workflow

1. Input student behavioral profile
2. System predicts grade category
3. AI explains prediction
4. User can ask follow-up questions

Example Prediction:

Prediction: Highest Performer

Explanation:
The student demonstrates strong study habits, high attendance, and strong exam performance.


---

## Project Structure


project/
│
├── core/
│ ├── orchestrator.py
│ ├── llm_client.py
│ ├── grade_predictor.py
│ └── train_model.py
│
├── modules/
│ └── memory.py
│
├── pipelines/
│ └── basic_chat.py
│
├── gui/
│ └── student_ai_console.py
│
├── dataset/
│ └── student_performance.csv
│
├── grade_model.pkl
└── main.py

---

## Installation

Clone the repository:


git clone https://github.com/yourusername/ai-academic-advisor


Install dependencies:


pip install -r requirements.txt


---

## Running the Project

Train the model:


python train_model.py


Run the AI system:


python main.py


Launch the GUI interface:


python student_ai_console.py


---

## Technologies Used

- Python
- Scikit-learn
- OpenAI API
- PyQt6
- Pandas
- NumPy

---

## Future Improvements

- Larger and more diverse datasets
- Real-time student monitoring
- Integration with educational platforms
- More advanced explainable AI techniques

---

## License (MIT)

This project was developed for educational and research purposes as part of a hackathon challenge.

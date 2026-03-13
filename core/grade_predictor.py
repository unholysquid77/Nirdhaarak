import joblib
import numpy as np

model = joblib.load("grade_model.pkl")

grade_map = {
    0: "Highest Performer",
    1: "Above Average",
    2: "Below Average",
    3: "At Risk"
}


def predict_grade(features):

    features = np.array(features).reshape(1, -1)

    pred = model.predict(features)[0]

    return grade_map[pred]
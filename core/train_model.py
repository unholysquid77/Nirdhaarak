import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("Loading dataset...")

df = pd.read_csv("student_performance.csv")

print("Dataset shape:", df.shape)

# -------------------------
# Separate features / target
# -------------------------

X = df.drop("FinalGrade", axis=1)
y = df["FinalGrade"]

# -------------------------
# Train/test split
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("Training samples:", len(X_train))

# -------------------------
# Model
# -------------------------

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

print("Training model...")

model.fit(X_train, y_train)

# -------------------------
# Evaluation
# -------------------------

preds = model.predict(X_test)

accuracy = accuracy_score(y_test, preds)

print("\nAccuracy:", accuracy)

print("\nClassification Report")
print(classification_report(y_test, preds))

# -------------------------
# Cross validation
# -------------------------

scores = cross_val_score(model, X, y, cv=5)

print("\nCross-val accuracy:", scores.mean())

# -------------------------
# Feature importance
# -------------------------

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(importance)

# -------------------------
# Save model
# -------------------------

joblib.dump(model, "../grade_model.pkl")

print("\nModel saved → grade_model.pkl")
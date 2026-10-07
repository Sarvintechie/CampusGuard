import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
print("=" * 50)
print(" CampusGuard AI Trainer V2 ")
print("=" * 50)

print("Loading Dataset...")

dataset = pd.read_csv(
    "merged_training_data.csv",
    header=None
)

print("Dataset Loaded Successfully!")

print("\nTotal Samples :", len(dataset))

print("Total Columns :", len(dataset.columns))

# -----------------------------
# Split Features and Labels
# -----------------------------

X = dataset.iloc[:, :-1]

y = dataset.iloc[:, -1]

print("\nFeatures Shape :", X.shape)

print("Labels Shape :", y.shape)

print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

print("\nTraining CampusGuard AI...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training Complete!")

joblib.dump(model, "violence_model_v2.pkl")

print("\nNew AI Model Saved!")
print("Filename : violence_model_v2.pkl")
print("\nEvaluating AI...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

print("\n" + "=" * 50)
print(" CampusGuard AI Evaluation ")
print("=" * 50)

print(f"Accuracy  : {accuracy*100:.2f}%")
print(f"Precision : {precision*100:.2f}%")
print(f"Recall    : {recall*100:.2f}%")
print(f"F1 Score  : {f1*100:.2f}%")

print("\nConfusion Matrix")
print(confusion_matrix(y_test, predictions))
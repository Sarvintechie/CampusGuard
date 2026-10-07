import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("====================================")
print(" CampusGuard AI Trainer ")
print("====================================")

print("Loading dataset...")

data = pd.read_csv(
    "dataset/training_data.csv",
    header=None
)

print(f"Total Samples : {len(data)}")

# Features (34 pose values)
X = data.iloc[:, :-1]

# Labels (0 = Normal, 1 = Violence)
y = data.iloc[:, -1]

print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Random Forest...")

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training Complete!")

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print()
print("==============================")
print(f"Accuracy : {accuracy*100:.2f}%")
print("==============================")
print()

print(classification_report(
    y_test,
    predictions
))

joblib.dump(
    model,
    "violence_model.pkl"
)

print("Model Saved Successfully!")
import joblib

from pose_features import PoseFeatureExtractor
from confidence_filter import ConfidenceFilter


class ViolenceAI:

    def __init__(self):

        print("Loading Trained AI Model...")

        self.model = joblib.load("violence_model.pkl")

        self.extractor = PoseFeatureExtractor()

        self.filter = ConfidenceFilter(history_size=15)

        print("AI Model Loaded Successfully!")

    def predict(self, result):

        features = self.extractor.extract(result)

        if features is None:
            return 0, "NORMAL"

        probability = self.model.predict_proba([features])[0][1]

        confidence = probability * 100

        # Smooth the prediction over the last 15 frames
        confidence = self.filter.update(confidence)

        if confidence >= 85:
            status = "EMERGENCY"

        elif confidence >= 70:
            status = "WARNING"

        else:
            status = "NORMAL"

        return confidence, status
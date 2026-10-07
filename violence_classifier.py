class ViolenceClassifier:

    def __init__(self):

        print("Violence Classifier Ready")

    def predict(self, sequence):

        if len(sequence) < 30:
            return "NORMAL", 0

        # Temporary dummy prediction
        return "NORMAL", 5
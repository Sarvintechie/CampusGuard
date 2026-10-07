import numpy as np


class PoseFeatureExtractor:

    def extract(self, result):

        if result.keypoints is None:
            return None

        keypoints = result.keypoints.xy

        if len(keypoints) == 0:
            return None

        person = keypoints[0].cpu().numpy()

        features = []

        for x, y in person:
            features.append(float(x))
            features.append(float(y))

        return np.array(features, dtype=np.float32)
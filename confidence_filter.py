import numpy as np


class ConfidenceFilter:

    def __init__(self, history_size=15):

        self.history_size = history_size
        self.history = []

    def update(self, confidence):

        self.history.append(confidence)

        if len(self.history) > self.history_size:
            self.history.pop(0)

        return float(np.mean(self.history))

    def reset(self):

        self.history.clear()
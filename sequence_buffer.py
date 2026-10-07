from collections import deque


class SequenceBuffer:

    def __init__(self, sequence_length=30):

        self.sequence_length = sequence_length

        self.buffer = deque(maxlen=sequence_length)

    def add(self, features):

        if features is None:
            return

        self.buffer.append(features)

    def is_ready(self):

        return len(self.buffer) == self.sequence_length

    def get_sequence(self):

        return list(self.buffer)

    def clear(self):

        self.buffer.clear()
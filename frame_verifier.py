class FrameVerifier:

    def __init__(self):

        self.consecutive_frames = 0
        self.required_frames = 5

    def verify(self, confidence, speed):

        # Check whether this frame looks suspicious
        suspicious = (
            confidence >= 75 and
            speed >= 20
        )

        if suspicious:
            self.consecutive_frames += 1
        else:
            # Slowly decrease instead of instantly resetting
            self.consecutive_frames = max(
                0,
                self.consecutive_frames - 1
            )

        verified = (
            self.consecutive_frames >=
            self.required_frames
        )

        return verified

    def get_progress(self):
        return (
            self.consecutive_frames,
            self.required_frames
        )
import cv2
import os
from datetime import datetime


class EvidenceRecorder:

    def __init__(self):

        self.recording = False
        self.writer = None

        os.makedirs("evidence", exist_ok=True)

    def start(self, frame):

        if self.recording:
            return

        filename = datetime.now().strftime(
            "evidence/fight_%Y%m%d_%H%M%S.mp4"
        )

        height, width = frame.shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self.writer = cv2.VideoWriter(
            filename,
            fourcc,
            20,
            (width, height)
        )

        self.recording = True

        print(f"Recording Started : {filename}")

    def write(self, frame):

        if self.recording and self.writer is not None:
            self.writer.write(frame)

    def stop(self):

        if self.recording:

            self.writer.release()

            self.recording = False

            print("Recording Saved")
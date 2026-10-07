import os
from datetime import datetime


class EventLogger:

    def __init__(self):

        os.makedirs("logs", exist_ok=True)

        self.file = "logs/events.txt"

        self.last_status = ""

    def write(

        self,

        threat,

        confidence,

        students

    ):

        # Don't write the same status every frame
        if threat == self.last_status:
            return

        self.last_status = threat

        current_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        with open(self.file, "a") as f:

            f.write("\n")

            f.write("=" * 40 + "\n")

            f.write(f"Time : {current_time}\n")

            f.write(f"Threat : {threat}\n")

            f.write(f"Fight Confidence : {confidence}%\n")

            f.write(f"Students : {students}\n")

            f.write("=" * 40 + "\n")

        print("Event Logged")
import math

class FightDetector:

    def __init__(self):

        self.previous_centers = {}

    def detect(self, student_data):

        confidence = 0

        if len(student_data) < 2:
            return 0, "NORMAL"

        speeds = []

        for student_id, center in student_data:

            if student_id not in self.previous_centers:

                self.previous_centers[student_id] = center
                speeds.append(0)
                continue

            old_x, old_y = self.previous_centers[student_id]
            new_x, new_y = center

            speed = math.sqrt(
                (new_x-old_x)**2 +
                (new_y-old_y)**2
            )

            speeds.append(speed)

            self.previous_centers[student_id] = center

        # Distance between first two students

        (id1, p1) = student_data[0]
        (id2, p2) = student_data[1]

        distance = math.sqrt(
            (p1[0]-p2[0])**2 +
            (p1[1]-p2[1])**2
        )

        average_speed = sum(speeds)/len(speeds)

        if distance < 150:
            confidence += 30

        if average_speed > 20:
            confidence += 25

        if average_speed > 40:
            confidence += 25

        if confidence >= 80:
            status = "URGENT"

        elif confidence >= 60:
            status = "WARNING"

        else:
            status = "NORMAL"

        return confidence, status
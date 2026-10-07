import math


class CrowdDetector:

    def __init__(self):

        self.distance_threshold = 170
        self.minimum_people = 3

    def detect(self, student_data):

        crowd_count = 0

        total = len(student_data)

        if total < self.minimum_people:
            return False, 0

        for i in range(total):

            nearby = 1

            id1, p1 = student_data[i]

            for j in range(total):

                if i == j:
                    continue

                id2, p2 = student_data[j]

                distance = math.sqrt(

                    (p1[0]-p2[0])**2 +
                    (p1[1]-p2[1])**2

                )

                if distance < self.distance_threshold:

                    nearby += 1

            if nearby >= self.minimum_people:

                crowd_count += 1

        return crowd_count > 0, crowd_count
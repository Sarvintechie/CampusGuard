class MovementAnalyzer:

    def __init__(self):
        self.previous_positions = {}

    def calculate_speed(self, student_id, center):

        if student_id not in self.previous_positions:
            self.previous_positions[student_id] = center
            return 0

        old_x, old_y = self.previous_positions[student_id]
        new_x, new_y = center

        speed = ((new_x - old_x) ** 2 + (new_y - old_y) ** 2) ** 0.5

        self.previous_positions[student_id] = center

        return speed
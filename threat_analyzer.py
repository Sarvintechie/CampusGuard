class ThreatAnalyzer:

    def __init__(self):
        pass

    def analyze(
        self,
        fight_confidence,
        crowd_count,
        average_speed
    ):

        score = 0

        # Fight Score
        score += fight_confidence

        # Crowd Score
        if crowd_count >= 8:
            score += 30

        elif crowd_count >= 5:
            score += 15

        # Movement Score
        if average_speed > 45:
            score += 20

        elif average_speed > 25:
            score += 10

        # Final Decision
        if score >= 80:
            return score, "EMERGENCY"

        elif score >= 50:
            return score, "WARNING"

        else:
            return score, "SAFE"
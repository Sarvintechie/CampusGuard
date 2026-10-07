print("THIS IS MY MAIN FILE")
import cv2
import time

from frame_verifier import FrameVerifier
from ultralytics import YOLO
from logger import EventLogger
from violence_ai import ViolenceAI
from movement_analyzer import MovementAnalyzer
from crowd_detector import CrowdDetector
from recorder import EvidenceRecorder
from threat_analyzer import ThreatAnalyzer
from pose_features import PoseFeatureExtractor
from dataset_collector import DatasetCollector

print("Loading CampusGuard AI...")

model = YOLO("yolo11n-pose.pt")

print("Model Loaded Successfully!")

violence_ai = ViolenceAI()
movement = MovementAnalyzer()
crowd_detector = CrowdDetector()
recorder = EvidenceRecorder()
brain = ThreatAnalyzer()
verifier = FrameVerifier()
feature_extractor = PoseFeatureExtractor()
collector = DatasetCollector()
logger = EventLogger()

print("Opening camera...")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Camera object created.")

print("Checking camera...")

print(cap.isOpened())

if not cap.isOpened():
    print("Cannot Open Camera")
    exit()

prev_time = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.track(frame, persist=True, tracker="bytetrack.yaml", verbose=False)

    display = frame.copy()

    student_count = 0
    total_speed = 0
    student_data = []

    for result in results:

        display = result.plot(boxes=False)
        features = feature_extractor.extract(result)

        if result.boxes is None:
            continue

        ids = result.boxes.id

        if ids is None:
            continue

        student_count = len(ids)

        for box, student_id in zip(result.boxes.xyxy, ids):

            x1, y1, x2, y2 = map(int, box)

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            speed = movement.calculate_speed(int(student_id), (center_x, center_y))

            total_speed += speed

            student_data.append((int(student_id), (center_x, center_y)))

            cv2.putText(
                display,
                f"Student {int(student_id)}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                display,
                f"Speed: {int(speed)}",
                (x1, y2 + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2,
            )

    confidence = 0
    status = "NORMAL"

    confidence = 0
    status = "NORMAL"

    for result in results:

        ai_confidence, ai_status = violence_ai.predict(result)

        if ai_confidence > confidence:
            confidence = ai_confidence
            status = ai_status

    if student_count > 0:
        average_speed = total_speed / student_count
    else:
        average_speed = 0
    crowd_detected, crowd_count = crowd_detector.detect(student_data)

    threat_score, threat_level = brain.analyze(confidence, crowd_count, average_speed)

    verified = verifier.verify(confidence, average_speed)

    # Ignore alerts until enough consecutive frames are detected
    if not verified:
        threat_level = "SAFE"

    if threat_level != "SAFE":
        logger.write(threat_level, confidence, student_count)

    # Auto Recording
    if verified:
        recorder.start(frame)
        recorder.write(frame)
    else:
        recorder.stop()

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    cv2.putText(
        display,
        f"Students : {student_count}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2,
    )

    cv2.putText(
        display,
        f"FPS : {int(fps)}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        display,
        f"Violence Confidence : {confidence:.1f}%",
        (20, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )

    if status == "EMERGENCY":
        status_color = (0, 0, 255)
    elif status == "WARNING":
        status_color = (0, 165, 255)
    else:
        status_color = (0, 255, 0)

    cv2.putText(
        display,
        f"Violence Status : {status}",
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        status_color,
        2,
    )

    if crowd_detected:
        crowd_text = f"Crowd : YES ({crowd_count})"
        crowd_color = (0, 0, 255)
    else:
        crowd_text = "Crowd : NO"
        crowd_color = (0, 255, 0)

    cv2.putText(
        display, crowd_text, (20, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.8, crowd_color, 2
    )

    cv2.putText(
        display,
        f"Threat Score : {int(threat_score)}",
        (20, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    if threat_level == "EMERGENCY":
        threat_color = (0, 0, 255)
    elif threat_level == "WARNING":
        threat_color = (0, 165, 255)
    else:
        threat_color = (0, 255, 0)

    cv2.putText(
        display,
        f"Threat Level : {threat_level}",
        (20, 255),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        threat_color,
        2,
    )
    current, required = verifier.get_progress()

    cv2.putText(
        display,
        f"Verification : {current}/{required}",
        (20, 325),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2,
    )
    if recorder.recording:
        cv2.putText(
            display, "REC ●", (20, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
        )

    cv2.imshow("CampusGuard AI", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("n"):
        collector.save(features, "normal")

    elif key == ord("v"):
        collector.save(features, "violence")

    elif key == ord("q"):
        break


cap.release()
recorder.stop()
cv2.destroyAllWindows()

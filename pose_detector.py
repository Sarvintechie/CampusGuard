import cv2
import time
from ultralytics import YOLO

# Load YOLO11 Pose model
model = YOLO("yolo11n-pose.pt")

# Open webcam (change 0 to your IP camera later)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Cannot open camera.")
    exit()

prev_time = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Run pose detection
    results = model(frame, verbose=False)

    # Create a clean copy of the frame
    display = frame.copy()

    # Draw ONLY pose skeletons (no boxes)
    for result in results:
        keypoints = result.keypoints

        if keypoints is not None:
            display = result.plot(boxes=False)

    # FPS Counter
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
    prev_time = current_time

    cv2.putText(
        display,
        f"FPS: {int(fps)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.imshow("CampusGuard - Pose Detection", display)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
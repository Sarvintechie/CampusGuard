import os
import cv2
import csv
from ultralytics import YOLO
from pose_features import PoseFeatureExtractor

print("=" * 50)
print(" CampusGuard Dataset Extraction Engine V2 ")
print("=" * 50)

print("Loading YOLO11 Pose Model...")

model = YOLO("yolo11n-pose.pt")

extractor = PoseFeatureExtractor()

print("YOLO Loaded Successfully!")
# Dataset Location

ROOT_FOLDER = "public_dataset/real life violence situations/Real Life Violence Dataset"

CLASSES = {
    "NonViolence": 0,
    "Violence": 1
}

OUTPUT_FILE = "public_pose_dataset.csv"

print("\nCreating output CSV...")

csv_file = open(OUTPUT_FILE, "w", newline="")

writer = csv.writer(csv_file)

total_samples = 0
total_videos = 0
for class_name, label in CLASSES.items():

    folder = os.path.join(ROOT_FOLDER, class_name)

    print(f"\nScanning {class_name}...")

    videos = sorted([
        f for f in os.listdir(folder)
        if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
    ])

    print(f"Found {len(videos)} videos")

    for video_name in videos[:5]:

        total_videos += 1

        video_path = os.path.join(folder, video_name)

        print(f"\nProcessing Video {total_videos}")

        print(video_name)
        cap = cv2.VideoCapture(video_path)

        frame_number = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame_number += 1

            # Process only every 5th frame
            if frame_number % 5 != 0:
                continue

            results = model(frame, verbose=False)

            for result in results:

                features = extractor.extract(result)

                if features is None:
                    continue

                row = features.tolist()
                row.append(label)

                writer.writerow(row)

                total_samples += 1

                if total_samples % 500 == 0:
                    print(f"Samples Extracted : {total_samples}")

        cap.release()

csv_file.close()

print("\n" + "=" * 50)
print("Extraction Complete!")
print("=" * 50)
print(f"Videos Processed : {total_videos}")
print(f"Samples Extracted : {total_samples}")
print(f"Saved To : {OUTPUT_FILE}")
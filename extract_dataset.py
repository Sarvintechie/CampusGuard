import os
import cv2
import csv

from ultralytics import YOLO
from pose_features import PoseFeatureExtractor

print("===================================")
print(" CampusGuard Dataset Extractor ")
print("===================================")

print("Loading YOLO Pose Model...")

model = YOLO("yolo11n-pose.pt")

print("Model Loaded Successfully!")

extractor = PoseFeatureExtractor()

VIOLENT_PATH = "public_dataset/hockey fight/violent"
NON_VIOLENT_PATH = "public_dataset/hockey fight/non violent"

OUTPUT_CSV = "dataset/training_data.csv"


def get_video_list(folder):

    videos = []

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        return videos

    for file in os.listdir(folder):

        if file.lower().endswith((".avi", ".mp4", ".mov", ".mkv")):

            videos.append(os.path.join(folder, file))

    return videos


def process_video(video_path, label, writer):

    print(f"Processing: {os.path.basename(video_path)}")

    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    saved_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Skip frames to make extraction faster
        if frame_count % 5 != 0:
            continue

        results = model(frame, verbose=False)

        for result in results:

            features = extractor.extract(result)

            if features is None:
                continue

            row = features.tolist()
            row.append(label)

            writer.writerow(row)
            saved_count += 1

    cap.release()

    print(f"Saved {saved_count} samples")


def main():

    violent_videos = get_video_list(VIOLENT_PATH)
    nonviolent_videos = get_video_list(NON_VIOLENT_PATH)

    print(f"Violent Videos     : {len(violent_videos)}")
    print(f"Non-Violent Videos : {len(nonviolent_videos)}")

    os.makedirs("dataset", exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        for video in violent_videos:
            process_video(video, 1, writer)

        for video in nonviolent_videos:
            process_video(video, 0, writer)

    print()
    print("===================================")
    print("Dataset Extraction Complete!")
    print(f"CSV Saved At : {OUTPUT_CSV}")
    print("===================================")


if __name__ == "__main__":
    main()
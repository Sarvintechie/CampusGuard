import os
import csv


class DatasetCollector:

    def __init__(self):

        os.makedirs("dataset/normal", exist_ok=True)
        os.makedirs("dataset/violence", exist_ok=True)

        print("Dataset Collector Ready!")

    def save(self, features, label):

        if features is None:
            return

        if label == "normal":
            filename = "dataset/normal/data.csv"
        else:
            filename = "dataset/violence/data.csv"

        with open(filename, "a", newline="") as file:

            writer = csv.writer(file)
            writer.writerow(features)

        print(f"Saved {label} sample")
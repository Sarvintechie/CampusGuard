import pandas as pd

print("NEW MERGE SCRIPT IS RUNNING")
print("=" * 50)
print(" CampusGuard Dataset Merger ")
print("=" * 50)

old_dataset = pd.read_csv("dataset/training_data.csv", header=None)
public_dataset = pd.read_csv("public_pose_dataset.csv", header=None)

print("Original Dataset :", len(old_dataset))
print("Public Dataset   :", len(public_dataset))

merged = pd.concat(
    [old_dataset, public_dataset],
    ignore_index=True
)

merged = merged.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

merged.to_csv(
    "merged_training_data.csv",
    index=False,
    header=False
)

print("\nMerge Successful!")

print("Total Samples :", len(merged))

print("\nSaved As")

print("merged_training_data.csv")
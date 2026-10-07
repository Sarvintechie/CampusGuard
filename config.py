"""
=========================================================
CampusGuard AI Configuration File
Author : Team CampusGuard
Version : 1.0
=========================================================
"""

# ===========================
# CAMERA SETTINGS
# ===========================

# 0 = Laptop Webcam
# Later replace with your IP Camera URL
CAMERA_SOURCE = 0

# Camera Name
CAMERA_NAME = "Main Entrance"

# ===========================
# AI SETTINGS
# ===========================

# YOLO Pose Model
MODEL_PATH = "yolo11n-pose.pt"

# Confidence Threshold
POSE_CONFIDENCE = 0.50

# ===========================
# FIGHT DETECTION SETTINGS
# ===========================

# Fight Confidence Levels
WARNING_LEVEL = 60
URGENT_LEVEL = 80

# Seconds students must behave aggressively
FIGHT_TIME_THRESHOLD = 2

# ===========================
# RECORDING SETTINGS
# ===========================

SAVE_VIDEO = True

SAVE_SCREENSHOT = True

EVIDENCE_FOLDER = "evidence"

# ===========================
# DASHBOARD SETTINGS
# ===========================

WINDOW_NAME = "CampusGuard AI"

SHOW_FPS = True

SHOW_STUDENT_ID = True

SHOW_CONFIDENCE = True

SHOW_STATUS = True

# ===========================
# WHATSAPP SETTINGS
# ===========================

ENABLE_WHATSAPP = False

# Add later
WHATSAPP_NUMBER = ""

# ===========================
# SYSTEM SETTINGS
# ===========================

PROJECT_NAME = "CampusGuard AI"

VERSION = "1.0"

SCHOOL_NAME = "Your School"

AUTHOR = "Team CampusGuard"

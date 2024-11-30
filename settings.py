# settings.py

# Train Settings
SPEED = 2  # Pixels per frame
TRAIN_IDS = ['train1', 'train2']  # IDs for the trains

# Waypoints without segment information
WAYPOINTS = {
    'train1': [
        (0,60), (10, 60), (30, 60), (50, 60), (100, 60), (120, 60), (160, 60), (180, 60), (200, 60), (250, 60)
    ],
    'train2': [
        (250, 70), (200, 70), (182, 70), (163, 70), (119, 70), (90, 70), (70, 70), (53, 70)
    ]
}

# Define segment relationships
SEGMENTS = {
    'train1': [
        "T1.S1", "T1.S2", "T1.S3", "T1.S4", "T1.S5", "T1.S6", "T1.S7", "T1.S8", "T1.S9", "T1.S9",
    ],
    'train2': [
        "T2.S8", "T2.S8", "T2.S7", "T2.S6", "T2.S5", "T2.S4", "T2.S3", "T2.S2", "T2.S1"
    ]
}

# Firebase Settings
DATABASE_URL = 'https://railflux-default-rtdb.asia-southeast1.firebasedatabase.app/'

y_digit = 460.79999999999995

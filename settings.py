# settings.py

# Train Settings
SPEED = 2  # Pixels per frame
TRAIN_IDS = ['train1', 'train2', 'train3']  # IDs for the trains

# Waypoints without segment information
WAYPOINTS = {
    'train1': [
        (0,60), (10, 60), (30, 60), (50, 60), (100, 60), (120, 60), (160, 60), (180, 60), (200, 60), (250, 60)
    ],
    'train2': [
        (250, 70), (200, 70), (182, 70), (163, 70), (119, 70), (90, 70), (70, 70), (53, 70)
    ],
    'train3': [
        (0,60), (10, 60), (30, 60), (50, 60), (100, 60), (110, 60), (130, 40), (135, 40), (150, 40), (170, 40), (190, 60), (200, 60), (250, 60)
    ]
}

SEGMENTS = {
    'train1': [
        "T1.S1", "T1.S2", "T1.S3", "T1.S4", "T1.S5", "T1.S6", "T1.S7", "T1.S8", "T1.S9", "T1.S9",
    ],
    'train2': [
        "T2.S8", "T2.S8", "T2.S7", "T2.S6", "T2.S5", "T2.S4", "T2.S3", "T2.S2", "T2.S1"
    ],
    'train3': [
        "T1.S1", "T1.S2", "T1.S3", "T1.S4", "T1.S5", "T5.S1", "T4.S2", "T4.S3", "T4.S4", "T6.S1", "T1.S8", "T1.S9"
    ]
}

# Firebase Settings
DATABASE_URL = 'https://railflux-default-rtdb.asia-southeast1.firebasedatabase.app/'

y_digit = 460.79999999999995

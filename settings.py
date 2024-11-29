# settings.py

# Train Settings
SPEED = 2  # Pixels per frame
TRAIN_IDS = ['train1', 'train2']  # IDs for the trains
WAYPOINTS = {
    'train1': [
        (0, 0), (0, 100), (100, 100), (100, 200), (200, 200)
    ],
    'train2': [
        (200, 200), (200, 100), (100, 100), (100, 0), (0, 0)
    ]
}

# Firebase Settings
DATABASE_URL = 'https://railflux-default-rtdb.asia-southeast1.firebasedatabase.app/'

# data_generator.py
import time
import math
from collections import deque
import firebase_setup  # Import Firebase setup to ensure Firebase is initialized
from firebase_admin import db
from metadata import GRIDSETTINGS, TRAINSETTINGS, WINDOWSETTINGS
from settings import TRAIN_IDS, WAYPOINTS, SEGMENTS

# Extracting metadata values
CELL_SIZE = GRIDSETTINGS['CELL_SIZE']
SPEED = TRAINSETTINGS['SPEED']

class Train:
    def __init__(self, train_id, speed, waypoints, segments, cell_size, num_wagons=10, spacing_interval=3):
        self.train_id = train_id
        self.speed = speed
        self.waypoints = self.convert_to_pixel(waypoints, cell_size)  # Convert waypoints to pixel coordinates
        self.segments = segments
        self.current_waypoint_index = 0
        self.position = list(self.waypoints[0])
        self.num_wagons = num_wagons
        self.positions = deque(maxlen=(num_wagons + 1) * spacing_interval)
        self.positions.append(self.position[:])
        self.spacing_interval = spacing_interval
        self.frame_counter = 0

        # Firebase reference for the train's data, each train has a unique path
        self.train_ref = db.reference(f'/trains/{self.train_id}')

        # Timer to control Firebase update frequency
        self.last_update_time = time.time()

    def convert_to_pixel(self, waypoints, cell_size):
        """Converts grid coordinates to pixel coordinates using the cell size."""
        return [(col * cell_size, row * cell_size) for col, row in waypoints]

    def move(self):
        if len(self.waypoints) == 0:
            return

        # Calculate the difference between current position and target waypoint
        target_x, target_y = self.waypoints[self.current_waypoint_index]
        delta_x = target_x - self.position[0]
        delta_y = target_y - self.position[1]
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        # If the train has reached the current waypoint, move to the next one
        if distance < self.speed:
            self.position = [target_x, target_y]
            self.update_firebase(self.current_waypoint_index)  # Update current segment in Firebase
            self.current_waypoint_index += 1

            # Check if we've reached the end of the track
            if self.current_waypoint_index >= len(self.waypoints):
                print(f"Train {self.train_id} reached end of track, resetting to start")
                # Reset to the first waypoint after reaching the last waypoint
                self.current_waypoint_index = 0
                # IMPORTANT: Immediately reset position to the starting waypoint
                self.position = list(self.waypoints[0])
                # Update Firebase with the reset position and first segment
                self.update_firebase(0)
            return

        # Normalize the direction vector and update the position of the train
        direction_x = delta_x / distance
        direction_y = delta_y / distance
        self.position[0] += direction_x * self.speed
        self.position[1] += direction_y * self.speed

        # Append the position to the list for wagons to follow
        self.frame_counter += 1
        if self.frame_counter >= self.spacing_interval:
            self.positions.append(self.position[:])
            self.frame_counter = 0

        # Update Firebase every second
        current_time = time.time()
        if current_time - self.last_update_time >= 1:  # Check if at least 1 second has passed
            self.update_firebase(self.current_waypoint_index)
            self.last_update_time = current_time

    def update_firebase(self, waypoint_index):
        # Calculate the correct segment index based on train movement direction
        segment_index = self.get_correct_segment_index(waypoint_index)

        # Ensure segment_index is within bounds
        if segment_index < 0 or segment_index >= len(self.segments):
            print(f"Warning: segment_index {segment_index} out of bounds for train {self.train_id}")
            return

        # Write current position, segment, and track to Firebase
        current_segment = self.segments[segment_index]
        track_id, segment_id = current_segment.split('.')

        self.train_ref.update({
            'current_position': {
                'x': self.position[0],
                'y': self.position[1]
            },
            'current_segment': segment_id,
            'current_track': track_id,
            'timestamp': time.time()
        })

    def get_correct_segment_index(self, waypoint_index):
        """
        Calculate the correct segment index based on movement direction.
        """
        # Determine movement direction by comparing first and last waypoints
        if len(self.waypoints) >= 2:
            start_x = self.waypoints[0][0]
            end_x = self.waypoints[-1][0]
            is_moving_right = end_x > start_x
        else:
            is_moving_right = True  # Default assumption

        if is_moving_right:
            # For left-to-right movement (like train1)
            # When train reaches waypoint N, it should occupy segment N-1
            # because it's currently in the segment it just traversed
            return max(0, waypoint_index - 1)
        else:
            # For right-to-left movement (like train2)
            # When train reaches waypoint N, it should occupy segment N
            # because segments are arranged to match the waypoint progression
            return waypoint_index


def main():
    # Initialize trains using waypoints and segments
    trains = [
        Train(
            train_id,
            SPEED,
            WAYPOINTS[train_id],
            SEGMENTS[train_id],
            CELL_SIZE  # Provide CELL_SIZE to convert coordinates to pixel values
        )
        for train_id in TRAIN_IDS
    ]

    start_delays = {
        'train1': 0,  # no delay
        'train2': 0,  # no delay
        'train3': 30  # 5-second delay
    }

    # Mark the time we started the script
    program_start_time = time.time()

    # Continuously move trains and update Firebase
    while True:
        current_time = time.time()
        for train in trains:
            # Check how many seconds have passed since script started
            elapsed = current_time - program_start_time

            # If not enough time has passed, skip moving this train
            if elapsed < start_delays.get(train.train_id, 0):
                continue

            train.move()
        time.sleep(0.1)  # Sleep for a short time to control the frequency of updates


if __name__ == "__main__":
    main()

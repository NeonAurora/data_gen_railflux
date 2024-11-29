# data_generator.py
import time
import math
from collections import deque
import firebase_setup  # Import Firebase setup to ensure Firebase is initialized
from firebase_admin import db
from settings import SPEED, TRAIN_IDS, WAYPOINTS


class Train:
    def __init__(self, train_id, speed, waypoints, num_wagons=10, spacing_interval=3):
        self.train_id = train_id
        self.speed = speed
        self.waypoints = waypoints
        self.current_waypoint_index = 0
        self.position = list(waypoints[0])
        self.num_wagons = num_wagons
        self.positions = deque(maxlen=(num_wagons + 1) * spacing_interval)
        self.positions.append(self.position[:])
        self.spacing_interval = spacing_interval
        self.frame_counter = 0

        # Firebase reference for the train's data, each train has a unique path
        self.train_ref = db.reference(f'/trains/{self.train_id}')

        # Timer to control Firebase update frequency
        self.last_update_time = time.time()

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
            self.current_waypoint_index += 1
            if self.current_waypoint_index >= len(self.waypoints):
                # Reset to the first waypoint after reaching the last waypoint
                self.current_waypoint_index = 0
                self.position = list(self.waypoints[0])
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
            self.update_firebase()
            self.last_update_time = current_time

    def update_firebase(self):
        # Write current position to Firebase
        self.train_ref.update({
            'current_position': {
                'x': self.position[0],
                'y': self.position[1]
            },
            'timestamp': time.time()
        })


def main():
    # Initialize trains
    trains = [Train(train_id, SPEED, WAYPOINTS[train_id]) for train_id in TRAIN_IDS]

    # Continuously move trains and update Firebase
    while True:
        for train in trains:
            train.move()
        time.sleep(0.1)  # Sleep for a short time to control the frequency of updates


if __name__ == "__main__":
    main()

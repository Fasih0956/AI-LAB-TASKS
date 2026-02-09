class Car:
    def __init__(self):
        self.lane = 2 
        self.speed = 60
        self.stopped = False

    def detect_obstacle(self, front=False, rear=False, left=False, right=False):
        if front:
            self.brake("Front obstacle detected")
        elif rear:
            self.brake("Rear obstacle detected")
        elif left:
            self.change_lane("right")
        elif right:
            self.change_lane("left")
        else:
            self.drive()

    def brake(self, reason):
        self.stopped = True
        self.speed = 0
        print(f"Brakes applied! Reason: {reason}")

    def change_lane(self, direction):
        if direction == "left" and self.lane > 1:
            self.lane -= 1
            print(f"Changing lane to left. Now in lane {self.lane}")
        elif direction == "right" and self.lane < 3:
            self.lane += 1
            print(f"Changing lane to right. Now in lane {self.lane}")
        else:
            print(f"Cannot change lane {direction}, staying in lane {self.lane}")

    def drive(self):
        self.stopped = False
        print(f"Driving in lane {self.lane} at speed {self.speed} km/h")

car = Car()

print("Initial state:")
car.drive()
print("---Obstacle Scenario---")

car.detect_obstacle(front=True)

car.speed = 60
car.stopped = False

car.detect_obstacle(left=True)

car.detect_obstacle(right=True)

car.detect_obstacle(rear=True)

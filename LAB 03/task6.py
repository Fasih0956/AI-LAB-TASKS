class Building:
    def __init__(self):
        self.rooms = {
            'a': 'safe', 'b': 'safe', 'c': 'fire',
            'd': 'safe', 'e': 'fire', 'f': 'safe',
            'g': 'safe', 'h': 'safe', 'j': 'fire'
        }
        self.grid_map = [
            ['a', 'b', 'c'],
            ['d', 'e', 'f'],
            ['g', 'h', 'j']
        ]
    def display(self):
        print("Current Building Status:")
        for row in self.grid_map:
            display_row = ""
            for room in row:
                if self.rooms[room] == 'fire':
                    display_row += "🔥 "
                else:
                    display_row += "🟩 "
            print(display_row)
        print("\n")

class FirefightingRobot:
    def __init__(self, building, path):
        self.building = building
        self.path = path
        self.position = path[0]

    def move_and_extinguish(self):
        for room in self.path:
            self.position = room
            print(f"Robot moved to room '{room}'.")

            if self.building.rooms[room] == 'fire':
                print(f"🔥 Fire detected in room '{room}'! Extinguishing...")
                self.building.rooms[room] = 'safe'
                print(f"✅ Fire in room '{room}' extinguished.")
            else:
                print(f"Room '{room}' is safe.")

            self.building.display()

path = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j']

building = Building()
robot = FirefightingRobot(building, path)

print("Initial Building Status:")
building.display()

robot.move_and_extinguish()

print("Final Building Status (all fires extinguished):")
building.display()

class Sensor:
    network_name = "XYZ NETWORK"
    def __init__(self , sensor_id , location , temperature):
        self.sensor_id = sensor_id
        self.location = location
        self.temperature = temperature
    def display_status(self):
     print(f"Sensor ID: {self.sensor_id}")
     print(f"Location: {self.location}")
     print(f"Temperature: {self.temperature} C")

s1 = Sensor(101 , "Karachi" , 25)     
s2 = Sensor(102 , "Lahore" , 30)     
s3 = Sensor(103 , "Sargodha" , 40)

print("---DISPLAYING SENSOR 1 STATUS---")
s1.display_status()
print("\n---DISPLAYING SENSOR 2 STATUS---")
s2.display_status()
print("\n---DISPLAYING SENSOR 3 STATUS---")
s3.display_status()

print("\n---SENSOR 1 TEMPERATURE BEFORE CHANGE---")
print(f"{s1.temperature} C")
s1.temperature = 45
print("---SENSOR 1 TEMPERATURE AFTER CHANGE---")
print(f"{s1.temperature} C")

print("\n---NETWORK NAME BEFORE CHANGE---")
print(Sensor.network_name)
Sensor.network_name = "ABC NETWORK"
print("---NETWORK NAME AFTER CHANGE---")
print(Sensor.network_name)









class Environment:
    def __init__(self):
        self.path_clear = True
        self.vehicle_tax_paid = False

    def set_vehicle(self, tax_paid, path_clear=True):
        self.vehicle_tax_paid = tax_paid
        self.path_clear = path_clear

    def display_status(self):
        print(f"Vehicle tax paid: {self.vehicle_tax_paid}")
        print(f"Path clear: {self.path_clear}")

class ModelAgent:
    def __init__(self, environment):
        self.env = environment

    def decide(self):
        if self.env.vehicle_tax_paid and self.env.path_clear:
            self.allow_vehicle()
        else:
            self.stop_vehicle()

    def allow_vehicle(self):
        print("Decision: Allow vehicle to pass. Gate opened!")

    def stop_vehicle(self):
        print("Decision: Stop vehicle. Gate closed!")

toll = Environment()
agent = ModelAgent(toll)

# different scenarios below

print("Scenario 1:")
toll.set_vehicle(tax_paid=True, path_clear=True)
toll.display_status()
agent.decide()
print()

print("Scenario 2:")
toll.set_vehicle(tax_paid=False, path_clear=True)
toll.display_status()
agent.decide()
print()

print("Scenario 3:")
toll.set_vehicle(tax_paid=True, path_clear=False)
toll.display_status()
agent.decide()
print()

print("Scenario 4:")
toll.set_vehicle(tax_paid=False, path_clear=False)
toll.display_status()
agent.decide()

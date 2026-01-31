class Cart:
    def __init__(self, total=0):
        self.__total = total
        self.items = {}

    def add_item(self, name, quantity, price):
        self.items[name] = {
            "Quantity": quantity,
            "Price": price
        }
        self.__total += quantity * price

    def remove_item(self, name):
        if name in self.items:
            item = self.items[name]
            self.__total -= item["Quantity"] * item["Price"]
            removed = self.items.pop(name)
            print(f"Removed Item: {name} -> {removed}")
        else:
            print(f"Item '{name}' not found.")

    def display_cart_info(self):
        print("Items Info:")
        for name, info in self.items.items():
            print(
                f"Name: {name}, "
                f"Quantity: {info['Quantity']}, "
                f"Unit Price: {info['Price']}"
            )
        print(f"Total: PKR {self.__total}")

it1 = Cart()

it1.add_item("Laptop", 2, 25000)
it1.add_item("Mouse", 1, 1500)
it1.add_item("Keyboard", 2, 1000)

print("---Displaying Cart Items---")
it1.display_cart_info()

print("\n---Removing Mouse---")
it1.remove_item("Mouse")

print("\n---Displaying Cart After removing Mouse---")
it1.display_cart_info()

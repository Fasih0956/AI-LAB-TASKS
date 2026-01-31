pi = 3.142
class Shape:
    def area():
        print("---Area of Shape---")
    def perimeter():
        print("---Perimeter of shape---")

class Square(Shape):
    def __init__(self , side):
        self.side = side
    def area(self):
        result = self.side * self.side
        return result
    def perimeter(self):
        result = 4 * self.side
        return result

class Rectangle(Shape):
    def __init__(self , len , wid):
        self.len = len
        self.wid = wid
    def area(self):
        result = self.len * self.wid
        return result
    def perimeter(self):
        result = 2 * (self.len + self.wid)
        return result

class Circle(Shape):
    def __init__(self , rad):
        self.rad = rad
    def area(self):
        result = pi * (self.rad * self.rad)
        return result
    def perimeter(self):
        result = 2 * pi * self.rad
        return result

class Triangle(Shape):   # considering triangle to be equilateral
    def __init__(self , base , height):
        self.base = base
        self.height = height
    def area(self):
        result = 0.5 * self.base * self.height
        return result
    def perimeter(self):
        result = 3 * self.base
        return result      
    
# All values typecasted to int for simplicity
s1 = Square(10)
print(f"Area of Square: ",int(s1.area()))
print(f"Perimeter of Square: ",int(s1.perimeter()))

r1 = Rectangle(5,10)
print(f"\nArea of Rectangle: ", int(r1.area()))
print(f"Perimeter of Rectangle: ",int(r1.perimeter()))

c1 = Circle(5)
print(f"\nArea of Circle: ",int(c1.area()))
print(f"Perimeter of Circle: ",int(c1.perimeter()))

t1 = Triangle(3,4)
print(f"\nArea of Equilateral Trianle: ",int(t1.area()))
print(f"Perimeter of Equilateral Triangle: ",int(t1.perimeter()))










 

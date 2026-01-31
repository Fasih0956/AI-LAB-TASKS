def addition(*args):  # can also use return sum(*args) because it is pre defined
    if len(args) == 0:
        return 0
    result = args[0]
    for num in args[1:]:
        result += num
    return result

def subtraction(*args):
    if len(args) == 0:
        return 0
    result = args[0]
    for num in args[1:]:
        result -= num
    return result

def multiply(*args):
    if len(args) == 0:
        return 0
    result = args[0]
    for num in args[1:]:
        result *= num
    return result
print("---PYHTON SIMPLE CALCULATOR---")
while True:
   print("\n1: Addition")
   print("2: Subtraction")
   print("3: Multiplication")
   print("4: Exit")
   op = input("Enter your choice: ")
   match op:
      case '1':
         nums = list(map(int, input("Enter numbers: ").split()))
         result = addition(*nums)
         print(f"The result of Addition is: {result}")
      case '2':
         nums = list(map(int, input("Enter numbers: ").split()))
         result = subtraction(*nums)
         print(f"The result of subtraction is: {result}")
      case '3':
         nums = list(map(int, input("Enter numbers: ").split()))
         result = multiply(*nums)
         print(f"The result of Multiplication is: {result}")  
      case '4':
           print("Exiting...")
           break
    













def read_matrix(n, name):
    print(f"Enter elements of {name} matrix:")
    matrix = []
    for i in range(n):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        matrix.append(row)
    return matrix
def add_matrices(mat1, mat2, n):
    result = [[0]*n for _ in range(n)] #initializing with 0 to avoid garbage
    for i in range(n):
        for j in range(n):
            result[i][j] = mat1[i][j] + mat2[i][j]
    return result
def subtract_matrices(mat1, mat2, n):
    result = [[0]*n for _ in range(n)]  # same as above
    for i in range(n):
        for j in range(n):
            result[i][j] = mat1[i][j] - mat2[i][j]
    return result
def print_matrix(matrix):
    for row in matrix:
        print(row)

n = int(input("Enter order of square matrix: "))
mat1 = read_matrix(n, "first")
mat2 = read_matrix(n, "second")

while True:
    print("MENU")
    print("1. Add matrices")
    print("2. Subtract matrices")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        result = add_matrices(mat1, mat2, n)
        print("Result of Addition:")
        print_matrix(result)
    elif choice == 2:
        result = subtract_matrices(mat1, mat2, n)
        print("Result of Subtraction:")
        print_matrix(result)
    elif choice == 3:
        print("Exited")
        break
    else:
        print("Invalid choice! Try again.")

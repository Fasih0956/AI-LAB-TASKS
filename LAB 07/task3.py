N = 6
SUB_ROW = 2
SUB_COL = 3

def print_board(board):
    for row in board:
        print(row)

def find_empty(board):
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return i, j
    return None

def is_valid(board, row, col, num):

    for j in range(N):
        if board[row][j] == num:
            return False

    for i in range(N):
        if board[i][col] == num:
            return False
        
    start_row = (row // SUB_ROW) * SUB_ROW
    start_col = (col // SUB_COL) * SUB_COL

    for i in range(start_row, start_row + SUB_ROW):
        for j in range(start_col, start_col + SUB_COL):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board):

    empty = find_empty(board)
    if not empty:
        return True

    row, col = empty

    for num in range(1, N + 1):

        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

board = [
    [0, 0, 6, 2, 0, 5],
    [0, 0, 0, 4, 6, 0],
    [0, 1, 2, 0, 0, 0],
    [5, 6, 0, 0, 0, 4],
    [0, 0, 4, 3, 0, 2],
    [3, 0, 0, 5, 0, 6]
]

if solve_sudoku(board):
    print("Solved Sudoku:")
    print_board(board)
else:
    print("No solution exists")
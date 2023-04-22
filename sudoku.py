import random


def is_valid_number(number, input_column_id, input_row_id, board: dict, mode: int):
    for column_id in range(9):
        if number == board[input_row_id][column_id]:
            if mode == 0:
                return False
            else:
                return [input_row_id, column_id]
    for row_id in range(9):
        if number == board[row_id][input_column_id]:
            if mode == 0:
                return False
            else:
                return [row_id, input_column_id]
    box_start_row = input_row_id//3*3
    box_start_col = input_column_id//3*3
    for i in range(3):
        for j in range(3):
            if board[i + box_start_row][j + box_start_col] == number:
                if mode == 0:
                    return False
                else:
                    return [i + box_start_row, j + box_start_col]
    return True



def one_step_generate_sudoku(board: dict):
    index = 0
    while index < 81:
        row_id = random.randint(0, 8)
        column_id = random.randint(0, 8)
        if board[row_id][column_id] == " ":
            generated_number = random.randint(1, 9)
            if is_valid_number(generated_number, column_id, row_id, board, 0):
                board[row_id][column_id] = generated_number
                index += 1
            else:
                for z in range(1,10):
                    if is_valid_number(z, column_id, row_id, board, 0):
                        board[row_id][column_id] = z
                        index += 1
                        break
                else:
                    coordinates = is_valid_number(generated_number, column_id, row_id, board, 1)
                    board[int(coordinates[0])][int(coordinates[1])] = " "
                    index -= 1
    return board


sudoku = {}
for rowIndex in range(9):
    rows = []
    for columnIndex in range(9):
        rows.append(" ")
    sudoku[rowIndex] = rows
one_step_generate_sudoku(sudoku)
a = 1
# import random

# Sudoku solver and game generator
# steps:
# 1. generate a random sudoku board
# 2. solve the board
# 3. remove numbers from the board
# 4. check if the board is still solvable
# 5. if not, go back to step 3
# 6. if yes, return the board

# difficulty_mode = {
#     'easy': 0.5,
#     'medium': 0.3,
#     'hard': 0.1
# }
#
# def is_valid_row(row_array):
#     my_map = {i: False for i in range(1, 10)}
#
#     for item in row_array:
#         if item is not None:
#             if my_map.get(item):
#                 return False
#             else:
#                 my_map[item] = True
#
#     return True
#
# def valid_board(board):
#     for pick_index in range(9):
#         row = board[pick_index]
#         if not is_valid_row(row):
#             return False
#
#         col = [row[pick_index] for row in board]
#         if not is_valid_row(col):
#             return False
#
#         rows = [
#             row for i, row in enumerate(board) if (pick_index // 3) * 3 <= i < (pick_index // 3) * 3 + 3
#         ]
#
#         square = [
#             [
#                 col for j, col in enumerate(row) if (pick_index % 3) * 3 <= j < (pick_index % 3) * 3 + 3
#             ]
#             for row in rows
#         ]
#
#         square_as_row = [item for sublist in square for item in sublist]
#
#         if not is_valid_row(square_as_row):
#             return False
#
#     return True
#
# def next_step(board, numbers_to_generate, numbers_count):
#     if numbers_count >= numbers_to_generate:
#         return False
#     row_index = random.randint(0, 8)
#     col_index = random.randint(0, 8)
#     number = random.randint(1, 9)
#
#     if board[row_index][col_index] is None:
#         board[row_index][col_index] = number
#         if valid_board(board):
#             if next_step(board, numbers_to_generate, numbers_count + 1):
#                 return True
#         board[row_index][col_index] = None
#         return True
#     return True
#
# def generate_board():
#     board = [[None for _ in range(9)] for _ in range(9)]
#
#     numbers_to_generate = int(81 * difficulty_mode['easy'])
#     step = 0
#     numbers_count = 0
#     while next_step(board, numbers_to_generate, numbers_count):
#         step += 1
#
#     return board
#
# board_to_solve = generate_board()
# print(board_to_solve)

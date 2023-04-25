import random
import tkinter as tk


def print_dictionary(board: dict):
    for i in range(9):
        print(board[i])


def validate_sudoku(board: dict):
    for current_row_id in range(9):
        for current_column_id in range(9):
            number = board[current_row_id][current_column_id]
            for column_id in range(9):
                if number == board[current_row_id][column_id]:
                    return False
            for row_id in range(9):
                if number == board[row_id][current_column_id]:
                    return False
            box_start_row = current_row_id // 3 * 3
            box_start_col = current_column_id // 3 * 3
            for i in range(3):
                for j in range(3):
                    if board[i + box_start_row][j + box_start_col] == number:
                        return False
            return True


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
    box_start_row = input_row_id // 3 * 3
    box_start_col = input_column_id // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[i + box_start_row][j + box_start_col] == number:
                if mode == 0:
                    return False
                else:
                    return [i + box_start_row, j + box_start_col]
    return True


def sudoku_solver(board: dict, numbers_solved: int):
    while numbers_solved < 81:
        row_id = random.randint(0, 8)
        column_id = random.randint(0, 8)
        if board[row_id][column_id] == " ":
            generated_number = random.randint(1, 9)
            if is_valid_number(generated_number, column_id, row_id, board, 0):
                board[row_id][column_id] = generated_number
                numbers_solved += 1
            else:
                for z in range(1, 10):
                    if is_valid_number(z, column_id, row_id, board, 0):
                        board[row_id][column_id] = z
                        numbers_solved += 1
                        break
                else:
                    coordinates = is_valid_number(generated_number, column_id, row_id, board, 1)
                    board[int(coordinates[0])][int(coordinates[1])] = " "
                    numbers_solved -= 1
    return board


sudoku = {}
for rowIndex in range(9):
    rows = []
    for columnIndex in range(9):
        rows.append(" ")
    sudoku[rowIndex] = rows
sudoku = sudoku_solver(sudoku, 0)

window = tk.Tk()

window.geometry("500x500")
window.title("Sudoku")

label = tk.Label(window, text="hello world!", font=("Arial", 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(window, height=3, font=("Arial", 16))
textbox.pack(padx=10)


button_frame = tk.Frame(window)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

button_1 = tk.Button(button_frame, text="1", font=("Arial", 15))
button_1.grid(row=0, column=0, sticky=tk.EW)

button_2 = tk.Button(button_frame, text="1", font=("Arial", 15))
button_2.grid(row=0, column=1, sticky=tk.EW)

button_3 = tk.Button(button_frame, text="1", font=("Arial", 15))
button_3.grid(row=1, column=0, sticky=tk.EW)

button_4 = tk.Button(button_frame, text="1", font=("Arial", 15))
button_4.grid(row=1, column=1, sticky=tk.EW)

button_frame.pack(fill="x")

button = tk.Button(window, text="test")
button.place(x=200, y=200, height=100, width=100)

window.mainloop()

class MyGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.mainloop()

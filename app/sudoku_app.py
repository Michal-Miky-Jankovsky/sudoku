import random
import copy
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


def is_valid_number(number, input_column_id, input_row_id, board: list, mode: int):
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


def sudoku_solver(board: list, numbers_solved: int):
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


def delete_from_sudoku(board: list, del_numbers: int):
    while del_numbers > 0:
        row_id = random.randint(0, 8)
        column_id = random.randint(0, 8)
        if board[row_id][column_id] == " ":
            pass
        else:
            board[row_id][column_id] = " "
            del_numbers -= 1
    return board


def sudoku_button(r, c):
    global buttons_grid
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "gray":
                buttons_grid[row][column]["bg"] = "white"
    if buttons_grid[r][c]["bg"] == "white":
        buttons_grid[r][c]["bg"] = "gray"


def number_button(c):
    global number_buttons, buttons_grid, users_sudoku
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "gray":
                buttons_grid[row][column]["text"] = number_buttons[c]["text"]
                buttons_grid[row][column]["bg"] = "white"


def difficulty_mode(dif):
    global difficulty
    difficulty = dif
    menu.destroy()


"""
difficulty menu
"""
difficulty = 0
menu = tk.Tk()
menu.title("Sudoku")
label = tk.Label(master=menu, text="choose a difficulty", font=("Arial", 30))
label.pack(padx=10, pady=10)
button_grid = tk.Frame(menu)
button_grid.rowconfigure(0, minsize=100, weight=1)
for h in range(3):
    button_grid.columnconfigure(h, minsize=100, weight=1)
Button_easy = tk.Button(master=button_grid, text="easy", font=("Arial", 18),
                        command=lambda dif=25: difficulty_mode(dif))
Button_easy.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
Button_medium = tk.Button(master=button_grid, text="medium", font=("Arial", 18),
                          command=lambda dif=35: difficulty_mode(dif))
Button_medium.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
Button_hard = tk.Button(master=button_grid, text="hard", font=("Arial", 18),
                        command=lambda dif=45: difficulty_mode(dif))
Button_hard.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
button_grid.pack(fill="x")
menu.mainloop()

"""
create sudoku
"""
sudoku = []
for rowIndex in range(9):
    rows = []
    for columnIndex in range(9):
        rows.append(" ")
    sudoku.append(rows)
sudoku = sudoku_solver(sudoku, 0)
finished_sudoku = copy.deepcopy(sudoku)
users_sudoku = copy.deepcopy(sudoku)
users_sudoku = delete_from_sudoku(users_sudoku, difficulty)


"""
game window
"""
window = tk.Tk()
window.title("Sudoku")
buttons_grid = []
sudoku_frame = tk.Frame(window)
for button_row in range(9):
    row_list = []
    for button_column in range(9):
        button = tk.Button(master=sudoku_frame, text=users_sudoku[button_row][button_column], height=3, width=6,
                           bg="white", command=lambda r=button_row, c=button_column: sudoku_button(r, c))
        button.grid(row=button_row, column=button_column)
        row_list.append(button)
    buttons_grid.append(row_list)
sudoku_frame.pack(fill="x", padx=70, pady=25)
for button_row in range(9):
    for button_column in range(9):
        if buttons_grid[button_row][button_column]["text"] == " ":
            pass
        else:
            buttons_grid[button_row][button_column]["bg"] = "#E3E3E3"

numbers_frame = tk.Frame(window)
number_buttons = []
for button_column in range(9):
    button = tk.Button(master=numbers_frame, text=button_column + 1, height=3, width=6,
                       command=lambda c=button_column: number_button(c))
    button.grid(row=0, column=button_column, padx=5)
    number_buttons.append(button)
numbers_frame.pack(fill="x", padx=25, pady=25)

menu_frame = tk.Frame(window)
hint_button = tk.Button(master=menu_frame, text="hint", height=3, width=10, command=hint)
hint_button.grid(row=0, column=0, padx=55)
restart_button = tk.Button(master=menu_frame, text="restart", height=3, width=10, command=restart)
restart_button.grid(row=0, column=1, padx=55)
solution_button = tk.Button(master=menu_frame, text="show solution", height=3, width=10, command=solution)
solution_button.grid(row=0, column=2, padx=55)
menu_frame.pack(fill="x", padx=20)
window.mainloop()

import keyboard as key
import tkinter as tk
import random
import copy


def validate_sudoku(board: list):
    for current_row_id in range(9):
        for current_column_id in range(9):
            if board[current_row_id][current_column_id] == " ":
                return False
            number = board[current_row_id][current_column_id]
            board[current_row_id][current_column_id] = " "
            if is_valid_number(number, current_column_id, current_row_id, board, 0):
                board[current_row_id][current_column_id] = number
            else:
                board[current_row_id][current_column_id] = number
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
    global buttons_grid, label, users_sudoku, bg
    label["text"] = " "
    if buttons_grid[r][c]["bg"] == "gray":
        buttons_grid[r][c]["text"] = " "
        users_sudoku[r][c] = " "
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "gray" or buttons_grid[row][column]["bg"] == "red":
                buttons_grid[row][column]["bg"] = bg
    if buttons_grid[r][c]["bg"] == bg:
        buttons_grid[r][c]["bg"] = "gray"


def number_button(c):
    global number_buttons, buttons_grid, users_sudoku, show, bg
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "gray":
                buttons_grid[row][column]["text"] = number_buttons[c]["text"]
                buttons_grid[row][column]["bg"] = bg
                users_sudoku[row][column] = number_buttons[c]["text"]
    if validate_sudoku(users_sudoku):
        show = True
        game_window.destroy()


def difficulty_mode(dif):
    global difficulty, start_game
    difficulty = dif
    start_game = True
    menu.destroy()


def help_button_def():
    global menu_end
    menu.destroy()
    menu_end = False
    help_menu = tk.Tk()
    help_menu.title("Sudoku help")
    help_label = tk.Label(master=help_menu, text="mazání čísel je dvojklikem\n"
                                                 "čísla se dají zadávat kliknutím na tlačítko nebo numpedem\n"
                                                 "bavte se :)", font=("Comic Sans MS", 16))
    help_label.pack(pady=10, padx=10)
    back_button = tk.Button(master=help_menu, text="back", font=("Comic Sans MS", 18), command=help_menu.destroy)
    back_button.pack()
    help_menu.mainloop()


def credits_button_def():
    global menu_end
    menu.destroy()
    menu_end = False
    credits_menu = tk.Tk()
    credits_menu.title("Sudoku credits")
    credits_label = tk.Label(master=credits_menu, text="autor: Jiří Černohorský\ndatum: 24.5.",
                             font=("Comic Sans MS", 16))
    credits_label.pack(pady=10, padx=10)
    back_button = tk.Button(master=credits_menu, text="back", font=("Comic Sans MS", 18), command=credits_menu.destroy)
    back_button.pack()
    credits_menu.mainloop()


def dark_mode_def():
    global menu_end, dark_mode_text
    menu.destroy()
    menu_end = False
    if dark_mode_text == "dark mode: off":
        dark_mode_text = "dark mode: on"
    else:
        dark_mode_text = "dark mode: off"


def mistakes():
    global users_sudoku, buttons_grid, label, bg
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == bg or\
               buttons_grid[row][column]["bg"] == "gray":
                if users_sudoku[row][column] == " ":
                    pass
                else:
                    number = users_sudoku[row][column]
                    users_sudoku[row][column] = " "
                    if is_valid_number(number, column, row, users_sudoku, 0):
                        users_sudoku[row][column] = number
                    else:
                        buttons_grid[row][column]["bg"] = "red"
                        users_sudoku[row][column] = number
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "red":
                label["text"] = "Red squares are mistakes."
                return
            else:
                label["text"] = "No mistakes found."


def restart():
    global buttons_grid, label, bg
    label["text"] = " "
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "red":
                buttons_grid[row][column]["bg"] = bg
                buttons_grid[row][column]["text"] = " "
            if buttons_grid[row][column]["bg"] == bg:
                buttons_grid[row][column]["text"] = " "


def solution():
    global buttons_grid, finished_sudoku, label, bg
    label["text"] = " "
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "red":
                buttons_grid[row][column]["bg"] = bg
                buttons_grid[row][column]["text"] = finished_sudoku[row][column]
            if buttons_grid[row][column]["bg"] == bg:
                buttons_grid[row][column]["text"] = finished_sudoku[row][column]


def new_game():
    global end
    end = False
    game_window.destroy()


def win_new_game():
    global end
    end = False
    end_window.destroy()


dark_mode_text = "dark mode: off"
for num in range(9):
    key.add_hotkey(str(num+1), lambda c=num: number_button(c))
while True:
    show = False
    end = True
    start_game = False

    """
    difficulty menu
    """
    while True:
        if dark_mode_text == "dark mode: off":
            bg = "white"
            fg = "black"
            bg_light = "#E3E3E3"
        else:
            bg = "black"
            fg = "white"
            bg_light = "#5A5A5A"
        menu_end = True
        difficulty = 0
        menu = tk.Tk()
        menu.title("Sudoku")
        menu.configure(bg=bg)
        label = tk.Label(master=menu, text="choose a difficulty", font=("Comic Sans MS", 30), bg=bg, fg=fg)
        label.pack(padx=10, pady=10)
        button_grid = tk.Frame(menu)
        button_grid.config(bg=bg)
        for h in range(3):
            button_grid.columnconfigure(h, minsize=100, weight=1)
        Button_easy = tk.Button(master=button_grid, text="easy", font=("Comic Sans MS", 18),
                                command=lambda dif=25: difficulty_mode(dif), bg=bg, fg=fg)
        Button_easy.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        Button_medium = tk.Button(master=button_grid, text="medium", font=("Comic Sans MS", 18),
                                  command=lambda dif=35: difficulty_mode(dif), bg=bg, fg=fg)
        Button_medium.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        Button_hard = tk.Button(master=button_grid, text="hard", font=("Comic Sans MS", 18),
                                command=lambda dif=45: difficulty_mode(dif), bg=bg, fg=fg)
        Button_hard.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        help_button = tk.Button(master=button_grid, text="help", font=("Comic Sans MS", 18), command=help_button_def,
                                bg=bg, fg=fg)
        help_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        dark_mode_button = tk.Button(master=button_grid, text=dark_mode_text, font=("Comic Sans MS", 18),
                                     command=dark_mode_def, bg=bg, fg=fg)
        dark_mode_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        credits_button = tk.Button(master=button_grid, text="credits", font=("Comic Sans MS", 18),
                                   command=credits_button_def, bg=bg, fg=fg)
        credits_button.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        button_grid.pack(fill="x")
        menu.mainloop()
        if menu_end:
            break

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
    if start_game:
        game_window = tk.Tk()
        game_window.title("Sudoku")
        game_window.configure(bg=bg)
        buttons_grid = []
        sudoku_frame = tk.Frame(game_window)
        sudoku_frame.config(bg=bg)
        for button_row in range(9):
            row_list = []
            for button_column in range(9):
                button = tk.Button(master=sudoku_frame, text=users_sudoku[button_row][button_column],
                                   font=("Comic Sans MS", 8), height=3, width=6, bg=bg, fg=fg,
                                   command=lambda r=button_row, c=button_column: sudoku_button(r, c))
                button.grid(row=button_row, column=button_column)
                row_list.append(button)
            buttons_grid.append(row_list)
        sudoku_frame.pack(fill="x", padx=70, pady=25)
        for button_row in range(9):
            for button_column in range(9):
                if buttons_grid[button_row][button_column]["text"] == " ":
                    pass
                else:
                    buttons_grid[button_row][button_column]["bg"] = bg_light

        label = tk.Label(game_window, text=" ", font=("Comic Sans MS", 14), bg=bg, fg=fg)
        label.pack()

        numbers_frame = tk.Frame(game_window)
        numbers_frame.config(bg=bg)
        number_buttons = []
        for button_column in range(9):
            button = tk.Button(master=numbers_frame, text=button_column + 1, font=("Comic Sans MS", 8), height=3, width=6,
                               command=lambda c=button_column: number_button(c), bg=bg, fg=fg)
            button.grid(row=0, column=button_column, padx=5)
            number_buttons.append(button)
        numbers_frame.pack(fill="x", padx=25, pady=20)

        menu_frame = tk.Frame(game_window)
        menu_frame.config(bg=bg)
        mistakes_button = tk.Button(master=menu_frame, text="find mistakes", font=("Comic Sans MS", 8),
                                    height=3, width=10, command=mistakes, bg=bg, fg=fg)
        mistakes_button.grid(row=0, column=0, padx=30)
        restart_button = tk.Button(master=menu_frame, text="restart", font=("Comic Sans MS", 8),
                                   height=3, width=10, command=restart, bg=bg, fg=fg)
        restart_button.grid(row=0, column=1, padx=30)
        solution_button = tk.Button(master=menu_frame, text="show solution", font=("Comic Sans MS", 8),
                                    height=3, width=10, command=solution, bg=bg, fg=fg)
        solution_button.grid(row=0, column=2, padx=30)
        new_game_button = tk.Button(master=menu_frame, text="new game", font=("Comic Sans MS", 8),
                                    height=3, width=10, command=new_game, bg=bg, fg=fg)
        new_game_button.grid(row=0, column=3, padx=30)
        menu_frame.pack(fill="x", padx=20)
        game_window.mainloop()

    if show:
        end_window = tk.Tk()
        end_window.title("Sudoku")
        end_window.config(bg=bg)
        win_label = tk.Label(end_window, text="you won", font=("Comic Sans MS", 30), bg=bg, fg=fg)
        win_label.pack(pady=10, padx=10)
        win_menu_frame = tk.Frame(end_window)
        win_menu_frame.config(bg=bg)
        win_new_game_button = tk.Button(master=win_menu_frame, text="new game", height=3, width=10,
                                        command=win_new_game, font=("Comic Sans MS", 18), bg=bg, fg=fg)
        win_new_game_button.grid(row=0, column=0, padx=5)
        exit_button = tk.Button(master=win_menu_frame, text="exit", height=3, width=10,
                                command=end_window.destroy, font=("Comic Sans MS", 18), bg=bg, fg=fg)
        exit_button.grid(row=0, column=1, padx=5)
        win_menu_frame.pack(fill="x", padx=10)
        end_window.mainloop()

    if end:
        break

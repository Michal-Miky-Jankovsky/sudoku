"""
Jiří Černohorský
program hry sudoku:
generace
UI
kontrola správnosti
"""
import keyboard as key
import tkinter as tk
import random
import copy


#prozkouší is_valid_number na celé sudoku
def validate_sudoku(board: list):
    for current_row_id in range(9):
        for current_column_id in range(9):
            if board[current_row_id][current_column_id] == " ":
                return False
            number = board[current_row_id][current_column_id]
            board[current_row_id][current_column_id] = " "      #odstraní číslo na aktuální pozici ze seznamu aby nenašlo is_valid_number samo sebe
            if is_valid_number(number, current_column_id, current_row_id, board, 0):
                board[current_row_id][current_column_id] = number
            else:
                board[current_row_id][current_column_id] = number
                return False
    return True


def is_valid_number(number, input_column_id, input_row_id, board: list, mode: int):
    #najde duplikáty v sloupci
    for column_id in range(9):
        if number == board[input_row_id][column_id]:
            if mode == 0:       #mode = 0 (detekuje duplikát)
                return False
            else:
                return [input_row_id, column_id]    #mode = 1 (vrátí pozici duplikátu)
    # najde duplikáty v řádku
    for row_id in range(9):
        if number == board[row_id][input_column_id]:
            if mode == 0:       #mode = 0 (detekuje duplikát)
                return False
            else:
                return [row_id, input_column_id]    #mode = 1 (vrátí pozici duplikátu)
    # najde duplikáty v boxu
    box_start_row = input_row_id // 3 * 3
    box_start_col = input_column_id // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[i + box_start_row][j + box_start_col] == number:
                if mode == 0:       #mode = 0 (detekuje duplikát)
                    return False
                else:
                    return [i + box_start_row, j + box_start_col]    #mode = 1 (vrátí pozici duplikátu)
    return True


def sudoku_solver(board: list, numbers_solved: int):
    while numbers_solved < 81:
        row_id = random.randint(0, 8)
        column_id = random.randint(0, 8)
        if board[row_id][column_id] == " ":
            generated_number = random.randint(1, 9)
            #dosadí generated_number na vygenerovanou pozici pokud je is_valid_number == True
            if is_valid_number(generated_number, column_id, row_id, board, 0):
                board[row_id][column_id] = generated_number
                numbers_solved += 1
            else:
                #pokusí se dosadit všechna čísla na vygenerovanou pozici
                for z in range(1, 10):
                    if is_valid_number(z, column_id, row_id, board, 0):
                        board[row_id][column_id] = z
                        numbers_solved += 1
                        break
                else:
                    #odstraní kolidující čislo s generated_number
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
    #pokud bylo tlačítko kliknuto 2x za sebou tak se "taxt" = " "
    if buttons_grid[r][c]["bg"] == "gray":
        buttons_grid[r][c]["text"] = " "
        users_sudoku[r][c] = " "
    for row in range(9):
        for column in range(9):
            #všechny obarvené kliknutelné tlačítka odbarví
            if buttons_grid[row][column]["bg"] == "gray" or buttons_grid[row][column]["bg"] == "red":
                buttons_grid[row][column]["bg"] = bg
    #obarví zmáčknuté tlačítko
    if buttons_grid[r][c]["bg"] == bg:
        buttons_grid[r][c]["bg"] = "gray"


def number_button(c):
    global number_buttons, buttons_grid, users_sudoku, show, bg
    for row in range(9):
        for column in range(9):
            #označenému tlačítku změní text na text zmáčknutého tlačítka s číslm
            if buttons_grid[row][column]["bg"] == "gray":
                buttons_grid[row][column]["text"] = number_buttons[c]["text"]
                buttons_grid[row][column]["bg"] = bg
                users_sudoku[row][column] = number_buttons[c]["text"]
    #zkontroluje jestli je sudoku dohrané
    if validate_sudoku(users_sudoku):
        show = True
        game_window.destroy()


def difficulty_mode(dif):
    global difficulty, start_game
    #nastaví difficulty podle dif zmáčknutého tlačítka
    difficulty = dif
    #zavře hlavní menu a zapne hru
    start_game = True
    menu.destroy()


def help_button_def():
    global menu_end, bg, fg
    #otevře menu s informacemi o hře
    menu.destroy()
    menu_end = False
    help_menu = tk.Tk()
    help_menu.title("Sudoku help")
    help_menu.config(bg=bg)
    help_menu.minsize(375, 185)
    help_menu.maxsize(375, 185)
    help_label = tk.Label(master=help_menu, text="double click deletes number.\n"
                                                 "numbers can be entered by clicking \na button or using a numpad.\n"
                                                 "Have fun. :)", font=("Arial", 16), bg=bg, fg=fg)
    help_label.pack(pady=10, padx=10)
    back_button = tk.Button(master=help_menu, text="back", font=("Arial", 18), command=help_menu.destroy,
                            bg=bg, fg=fg)
    back_button.pack()
    help_menu.mainloop()



def dark_mode_def():
    #změní barvu všech menu
    global menu_end, dark_mode_text
    menu.destroy()
    menu_end = False     #zapne znovu otevření hlavního menu
    if dark_mode_text == "dark mode: off":
        dark_mode_text = "dark mode: on"
    else:
        dark_mode_text = "dark mode: off"


def mistakes():
    global users_sudoku, buttons_grid, label, bg
    #projde všechna kliknutelná tlačítka v sudoku a najde jestli kolidují s jinými a případně je označí červeně
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
    #na základě toho jestli hjsou nějaká tlačítka označená červeně změní label["text"]
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "red":
                label["text"] = "Red squares are mistakes."
                return
            else:
                label["text"] = "No mistakes found."


def restart():
    global buttons_grid, label, bg, users_sudoku
    label["text"] = " "
    #všem kliknutelným tlačítkám se změní text na " "
    for row in range(9):
        for column in range(9):
            if buttons_grid[row][column]["bg"] == "red":
                buttons_grid[row][column]["bg"] = bg
                buttons_grid[row][column]["text"] = " "
                users_sudoku[row][column] = " "
            if buttons_grid[row][column]["bg"] == bg:
                buttons_grid[row][column]["text"] = " "
                users_sudoku[row][column] = " "


def solution():
    global buttons_grid, finished_sudoku, label, bg, bg_light
    #dopliní sudoku podle finished_sudoku a udělá je nekliknutelná
    for row in range(9):
        for column in range(9):
            buttons_grid[row][column]["bg"] = bg
            buttons_grid[row][column]["text"] = finished_sudoku[row][column]
            buttons_grid[row][column]["command"] = button_pass
    menu_frame.destroy()
    numbers_frame.destroy()
    label.destroy()
    #vrátí se do hlavního menu
    solution_new_game_button = tk.Button(master=game_window, text="new game", font=("Arial", 12),
                                         height=3, width=15, command=new_game, bg=bg, fg=fg)
    solution_new_game_button.pack(pady=15)


def new_game():
    global end
    end = False
    game_window.destroy()


def win_new_game():
    global end
    end = False
    end_window.destroy()


def button_pass():
    #nekliknutelná tlačítka
    pass

#prvotní výchozí nastavení
dark_mode_text = "dark mode: off"

#vytvoří hotkey pro numpad
for num in range(9):
    key.add_hotkey(str(num+1), lambda c=num: number_button(c))
while True:
    #výchozí nastavení při každé nové hře
    show = False
    end = True
    start_game = False

    """
    menu obtížnosti
    """
    while True:
        #nastavení barvy všech menu
        if dark_mode_text == "dark mode: off":
            bg = "white"
            fg = "black"
            bg_light = "#E3E3E3"
            sudoku_bg = "black"
        else:
            bg = "black"
            fg = "white"
            bg_light = "#5A5A5A"
            sudoku_bg = "white"
        #výchozí nastavení při každém vstupu do hlavního menu
        menu_end = True
        difficulty = 0
        menu = tk.Tk()
        menu.title("Sudoku")
        menu.configure(bg=bg)
        menu.minsize(375, 185)
        menu.maxsize(375, 185)
        #nadpis
        label = tk.Label(master=menu, text="choose a difficulty", font=("Arial", 30), bg=bg, fg=fg)
        label.pack(padx=10, pady=10)
        #nastavit grid tlačítek
        button_grid = tk.Frame(menu)
        button_grid.config(bg=bg)
        for h in range(3):
            button_grid.columnconfigure(h, minsize=100, weight=1)
        #tlačítka s obtížností
        Button_easy = tk.Button(master=button_grid, text="easy", font=("Arial", 18),
                                command=lambda dif=1: difficulty_mode(dif), bg=bg, fg=fg)
        Button_easy.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        Button_medium = tk.Button(master=button_grid, text="medium", font=("Arial", 18),
                                  command=lambda dif=35: difficulty_mode(dif), bg=bg, fg=fg)
        Button_medium.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        Button_hard = tk.Button(master=button_grid, text="hard", font=("Arial", 18),
                                command=lambda dif=45: difficulty_mode(dif), bg=bg, fg=fg)
        Button_hard.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        #help menu
        help_button = tk.Button(master=button_grid, text="help", font=("Arial", 18), command=help_button_def,
                                bg=bg, fg=fg)
        help_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        #tlačítko na nastavení barvy všech menu
        dark_mode_button = tk.Button(master=button_grid, text=dark_mode_text, font=("Arial", 18),
                                     command=dark_mode_def, bg=bg, fg=fg)
        dark_mode_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        button_grid.pack(fill="x")
        menu.mainloop()
        if menu_end:
            break

    """
    vytvoří sudoku
    """
    sudoku = []
    for rowIndex in range(9):
        rows = []
        for columnIndex in range(9):
            rows.append(" ")
        sudoku.append(rows)
    sudoku = sudoku_solver(sudoku, 0)   #vygeneruje vyplněné sudoku
    finished_sudoku = copy.deepcopy(sudoku)
    users_sudoku = copy.deepcopy(sudoku)
    users_sudoku = delete_from_sudoku(users_sudoku, difficulty) #umaže čísla ze sudoku podle obtížnosti

    """
    herní okno
    """
    if start_game:
        game_window = tk.Tk()
        game_window.title("Sudoku")
        game_window.configure(bg=bg)
        game_window.minsize(560, 730)
        game_window.maxsize(560, 730)
        buttons_grid = []
        #grid tlačítek sudoku
        sudoku_frame = tk.Frame(game_window)
        sudoku_frame.config(bg=sudoku_bg)
        for box_row in range(3):
            row_list1 = []
            row_list2 = []
            row_list3 = []
            for box_column in range(3):
                #grid tlačítek v jednotlivém boxu
                box = tk.Frame(sudoku_frame)
                box.config(bg=bg)
                for button_row in range(3):
                    for button_column in range(3):
                        #nastavení tlačítek v sudoku
                        button = tk.Button(master=box, text=users_sudoku[button_row+box_row*3][button_column+box_column*3],
                                           font=("Arial", 8), height=3, width=6, bg=bg, fg=fg,
                                           command=lambda r=button_row+box_row*3, c=button_column+box_column*3: sudoku_button(r, c))
                        button.grid(row=button_row, column=button_column)
                         #vkládání tlačítek do listu podle řádku
                        if button_row == 0:
                            row_list1.append(button)
                        elif button_row == 1:
                            row_list2.append(button)
                        else:
                            row_list3.append(button)
                box.grid(row=box_row, column=box_column, padx=1, pady=1)
            #vložení tří řádků do matice
            buttons_grid.append(row_list1)
            buttons_grid.append(row_list2)
            buttons_grid.append(row_list3)
        sudoku_frame.pack(fill="x", padx=70, pady=25)
        for button_row in range(9):
            for button_column in range(9):
                #pokud text tlačítka není " " udělá z něj neklikatelné a označí ho
                if buttons_grid[button_row][button_column]["text"] != " ":
                    buttons_grid[button_row][button_column]["bg"] = bg_light
                    buttons_grid[button_row][button_column]["command"] = button_pass

        #nastavení popisku
        label = tk.Label(game_window, text=" ", font=("Arial", 14), bg=bg, fg=fg)
        label.pack()

        #grid tlačítek s čísly
        numbers_frame = tk.Frame(game_window)
        numbers_frame.config(bg=bg)
        number_buttons = []
        for button_column in range(9):
            #nastavení tlačítek s čísly
            button = tk.Button(master=numbers_frame, text=button_column + 1, font=("Arial", 8), height=3,
                               width=6, command=lambda c=button_column: number_button(c), bg=bg, fg=fg)
            button.grid(row=0, column=button_column, padx=5)
            number_buttons.append(button)
        numbers_frame.pack(fill="x", padx=25, pady=20)

        #nastavení menu tlačítek
        menu_frame = tk.Frame(game_window)
        menu_frame.config(bg=bg)
        #vahledá kolidující čísla
        mistakes_button = tk.Button(master=menu_frame, text="find mistakes", font=("Arial", 8),
                                    height=3, width=10, command=mistakes, bg=bg, fg=fg)
        mistakes_button.grid(row=0, column=0, padx=30)
        #restartuj sudoku do původního stavu
        restart_button = tk.Button(master=menu_frame, text="restart", font=("Arial", 8),
                                   height=3, width=10, command=restart, bg=bg, fg=fg)
        restart_button.grid(row=0, column=1, padx=30)
        #ukáže řešení sudoku
        solution_button = tk.Button(master=menu_frame, text="solution", font=("Arial", 8),
                                    height=3, width=10, command=solution, bg=bg, fg=fg)
        solution_button.grid(row=0, column=2, padx=30)
        #vrátí se do hlavního menu
        new_game_button = tk.Button(master=menu_frame, text="new game", font=("Arial", 8),
                                    height=3, width=10, command=new_game, bg=bg, fg=fg)
        new_game_button.grid(row=0, column=3, padx=30)
        menu_frame.pack(fill="x", padx=20)
        game_window.mainloop()

    """
        výherní okno
    """
    if show:
        end_window = tk.Tk()
        end_window.title("Sudoku")
        end_window.config(bg=bg)
        end_window.minsize(340, 185)
        end_window.maxsize(340, 185)
        #nadpis
        win_label = tk.Label(end_window, text="you won", font=("Arial", 30), bg=bg, fg=fg)
        win_label.pack(pady=10, padx=10)
        #grid tlačítek  menu
        win_menu_frame = tk.Frame(end_window)
        win_menu_frame.config(bg=bg)
        #vrátí se do hlavního menu
        win_new_game_button = tk.Button(master=win_menu_frame, text="new game", height=3, width=10,
                                        command=win_new_game, font=("Arial", 18), bg=bg, fg=fg)
        win_new_game_button.grid(row=0, column=0, padx=5)
        #zavře hru
        exit_button = tk.Button(master=win_menu_frame, text="exit", height=3, width=10,
                                command=end_window.destroy, font=("Arial", 18), bg=bg, fg=fg)
        exit_button.grid(row=0, column=1, padx=5)
        win_menu_frame.pack(fill="x", padx=10)
        end_window.mainloop()

    if end:
        break

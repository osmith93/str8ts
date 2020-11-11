import tkinter as tk
from tkinter import filedialog, CENTER, BOTH, Grid, font
from game import Game


class BoxUI:
    fontname = "Times"
    smallsize = 9
    largesize = 28

    def __init__(self, parent, cell: tuple, value, empty, blocked, guesses):
        print(".", end="")
        self.cell = cell
        x, y = cell
        self.parent = parent
        self.value = value
        self.blocked = blocked
        self.empty = empty
        self.guesses = guesses

        if self.blocked:
            self.fontcolor = "white"
            self.color = "black"
        else:
            self.fontcolor = "black"
            self.color = "white"

        self.cell_frame = tk.Frame(parent, bg="black")
        self.cell_frame.grid(row=y, column=x, sticky="nsew")

        self.cell_inner_frame = tk.Frame(self.cell_frame, bg=self.color)
        self.cell_inner_frame.place(relwidth=0.96, relheight=0.96, relx=0.02, rely=0.02)

        self.draw()

    def redraw(self, value, empty, blocked, guesses):
        something_changed = False
        if self.value != value:
            something_changed = True
        if self.empty != empty:
            something_changed = True
        if self.blocked != blocked:
            something_changed = True
        if len(self.guesses) != len(guesses):
            something_changed = True
        something_changed = True
        self.value = value
        self.blocked = blocked
        self.empty = empty
        self.guesses = guesses

        if something_changed:
            self.draw()

    def draw(self):
        for widget in self.cell_inner_frame.winfo_children():
            widget.destroy()

        if self.blocked or not self.empty:
            for guess_x in range(3):
                self.cell_inner_frame.columnconfigure(guess_x, weight=0)
                self.cell_inner_frame.rowconfigure(guess_x, weight=0)
            self.cell_inner_frame.columnconfigure(0, weight=1)
            self.cell_inner_frame.rowconfigure(0, weight=1)
            if self.empty:
                text = ""
            else:
                text = str(self.value)
            label = tk.Label(self.cell_inner_frame, text=text, bg=self.color, fg=self.fontcolor,
                             font=(self.fontname, self.largesize))
            label.grid(column=0, row=0)
        else:
            for guess_x in range(3):
                self.cell_inner_frame.columnconfigure(guess_x, weight=1)
                self.cell_inner_frame.rowconfigure(guess_x, weight=1)
                for guess_y in range(3):
                    number = 1 + guess_x + 3 * guess_y
                    if number in self.guesses:
                        text = str(number)
                    else:
                        text = ""
                    label = tk.Label(self.cell_inner_frame, text=text, bg=self.color, fg=self.fontcolor,
                                     font=(BoxUI.fontname, BoxUI.smallsize))
                    label.grid(column=guess_x, row=guess_y)


class GameUI:
    primary = "#283593"
    primary_dark = "#001064"
    primary_light = "#5f5fc4"
    text_on_primary = "white"

    secondary = "#8e24aa"
    secondary_dark = "#5c007a"
    secondary_light = "#c158dc"
    text_on_secondary = "black"

    def __init__(self, game, solver):
        self.solver = solver
        self.game = game
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=700, width=700, bg=GameUI.primary)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.frame = tk.Frame(self.canvas, bg="white")
        self.frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        for x in range(game.size):
            Grid.columnconfigure(self.frame, x, weight=1)
            Grid.rowconfigure(self.frame, x, weight=1)

        self.boxes = []
        for x in range(game.size):
            for y in range(game.size):
                cell = (x, y)
                self.boxes.append(BoxUI(self.frame, cell, self.game.get_cell(cell), self.game.is_empty,
                                        self.game.is_blocked(cell), self.game.get_guesses(cell)))

        self.openFile = tk.Button(self.root, text="Update UI", padx=10, pady=5, fg=GameUI.text_on_primary,
                                  bg=GameUI.primary, activebackground=GameUI.primary_light,
                                  command=self.draw)
        self.openFile.grid(row=1, column=0)
        self.saveFile = tk.Button(self.root, text="Next Move", padx=10, pady=5, fg=GameUI.text_on_primary,
                                  bg=GameUI.primary, activebackground=GameUI.primary_light,
                                  command=self.next_step)
        self.saveFile.grid(row=1, column=1)

        self.root.mainloop()

    def next_step(self):
        self.solver.next_step()
        self.draw()

    def draw(self):
        for box in self.boxes:
            cell = box.cell
            box.redraw(self.game.get_cell(cell), self.game.is_empty, self.game.is_blocked(cell),
                       self.game.get_guesses(cell))

    def draw_old(self):
        n = self.game.size
        for x in range(n):
            for y in range(n):
                fontname = "Times New Roman"
                fontsize = 28
                if self.game.is_blocked((x, y)):
                    color = "black"
                    text_color = "white"
                else:
                    color = "white"
                    text_color = "black"
                if self.game.get_cell((x, y)) == Game.EMPTY:
                    text = ""
                    if not self.game.is_blocked((x, y)):
                        text = ",".join([str(g) for g in self.game.get_guesses((x, y))])
                        fontsize = 5
                        text_color = "gray"

                else:
                    text = str(self.game.get_cell((x, y)))

                cell_frame = tk.Frame(self.frame, bg="black")
                cell_frame.grid(row=y, column=x, sticky="nsew")
                cell_inner_frame = tk.Frame(cell_frame, bg=color)
                cell_inner_frame.place(relwidth=0.96, relheight=0.96, relx=0.02, rely=0.02)
                cell_inner_frame.columnconfigure(0, weight=1)
                cell_inner_frame.rowconfigure(0, weight=1)
                if self.game.get_cell((x, y)) == Game.EMPTY and not self.game.is_blocked((x, y)):
                    for guess_x in range(3):
                        cell_inner_frame.columnconfigure(guess_x, weight=1)
                        cell_inner_frame.rowconfigure(guess_x, weight=1)
                        for guess_y in range(3):
                            number = 1 + guess_x + 3 * guess_y
                            if number in self.game.get_guesses((x, y)):
                                text = str(number)
                            else:
                                text = ""
                            label = tk.Label(cell_inner_frame, text=text, bg=color, fg=text_color, font=(fontname, 9))
                            label.grid(column=guess_x, row=guess_y)
                else:
                    label = tk.Label(cell_inner_frame, text=text, bg=color, fg=text_color,
                                     font=(fontname, fontsize))
                    label.grid(column=0, row=0)

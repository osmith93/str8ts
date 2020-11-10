import tkinter as tk
from tkinter import filedialog, CENTER, BOTH, Grid, font
from utils import Game


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
        n = self.game.size
        for x in range(n):
            for y in range(n):
                fontname = "Times New Roman"
                fontsize = 28
                if self.game.is_cell_blocked((x, y)):
                    color = "black"
                    text_color = "white"
                else:
                    color = "white"
                    text_color = "black"
                if self.game.cell((x, y)) == Game.EMPTY:
                    text = ""
                    if not self.game.is_cell_blocked((x, y)):
                        text = ",".join([str(g) for g in self.game.guesses_in_cell((x, y))])
                        fontsize = 5
                        text_color = "gray"

                else:
                    text = str(self.game.cell((x, y)))

                cell_frame = tk.Frame(self.frame, bg="black")
                cell_frame.grid(row=y, column=x, sticky="nsew")
                cell_inner_frame = tk.Frame(cell_frame, bg=color)
                cell_inner_frame.place(relwidth=0.96, relheight=0.96, relx=0.02, rely=0.02)
                cell_inner_frame.columnconfigure(0, weight=1)
                cell_inner_frame.rowconfigure(0, weight=1)
                if self.game.cell((x, y)) == Game.EMPTY and not self.game.is_cell_blocked((x, y)):
                    for guess_x in range(3):
                        cell_inner_frame.columnconfigure(guess_x, weight=1)
                        cell_inner_frame.rowconfigure(guess_x, weight=1)
                        for guess_y in range(3):
                            number = 1 + guess_x + 3 * guess_y
                            if number in self.game.guesses_in_cell((x, y)):
                                text = str(number)
                            else:
                                text = ""
                            label = tk.Label(cell_inner_frame, text=text, bg=color, fg=text_color, font=(fontname, 9))
                            label.grid(column=guess_x, row=guess_y)
                else:
                    label = tk.Label(cell_inner_frame, text=text, bg=color, fg=text_color,
                                     font=(fontname, fontsize))
                    label.grid(column=0, row=0)

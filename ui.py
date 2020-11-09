import tkinter as tk
from tkinter import filedialog, CENTER, BOTH, Grid
from utils import Game


class GameUI:
    primary = "#0d47a1"
    primary_dark = "#002171"
    primary_light = "#5472d3"
    text_on_primary = "white"

    secondary = "#29b6f6"
    secondary_dark = "#0086c3"
    secondary_light = "#73e8ff"
    text_on_secondary = "black"


    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=700, width=700, bg=GameUI.primary)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.frame = tk.Frame(self.canvas, bg="white")
        self.frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        for x in range(game.size):
            Grid.columnconfigure(self.frame, x, weight=1)
            Grid.rowconfigure(self.frame, x, weight=1)

        self.openFile = tk.Button(self.root, text="Load Game", padx=10, pady=5, fg=GameUI.text_on_primary, bg=GameUI.primary, activebackground=GameUI.primary_light,
                                  command=self.draw)
        self.openFile.grid(row=1, column=0)
        self.saveFile = tk.Button(self.root, text="Save Game", padx=10, pady=5, fg=GameUI.text_on_primary, bg=GameUI.primary, activebackground=GameUI.primary_light)
        self.saveFile.grid(row=1, column=1)

        self.root.mainloop()

    def draw(self):
        #for widget in self.frame.winfo_children():
        #    widget.destroy()
        n = self.game.size
        for x in range(n):
            for y in range(n):
                color = GameUI.primary_dark
                if self.game.cell(x,y) == Game.EMPTY:
                    text = ""
                elif self.game.cell(x,y) == Game.BLOCKED:
                    text = ""
                    color = "black"
                else:
                    text = str(self.game.cell(x,y))

                cell_frame = tk.Frame(self.frame, bg="gray")
                cell_frame.grid(row=y, column=x, sticky="nsew")
                cell_inner_frame = tk.Frame(cell_frame, bg=color)
                cell_inner_frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)
                cell_inner_frame.columnconfigure(0, weight=1)
                cell_inner_frame.rowconfigure(0, weight=1)

                label = tk.Label(cell_inner_frame, text=text, bg=color, fg="white", font=("Courier",15))
                label.grid(column=0, row=0)
#        cell_frame.grid(sticky="nsew")

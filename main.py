import pygameui
from game import Game
from solver import Solver

if __name__ == '__main__':
    game = Game()
    game.load("./data/board01.txt")
    solver = Solver(game)
    ui = pygameui.UI(game, solver)
    ui.on_execute()

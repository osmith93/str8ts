import ui
from game import Game
from solver import Solver

if __name__ == '__main__':
    game = Game()
    game.load("./data/board01.txt")
    solver = Solver(game.board)
    app = ui.UI(game, solver)
    app.on_execute()

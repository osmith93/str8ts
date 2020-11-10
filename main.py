import ui
from utils import Game

if __name__ == '__main__':
    game = Game()
    game.load("./data/board01.txt")
    ui = ui.GameUI(game)

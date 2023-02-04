from Game import Game
from original_game import OriginalGame

class ImplementationUtils():
    def __init__(self):
        pass

    def cell_state_to_2d(self, cell_state):
        pass

class ImplementedGame(Game):
    def __init__(self):
        pass

    def getInitBoard(self):
        original_game = OriginalGame()
        print(original_game.cell_state)


implemented_game = ImplementedGame()
implemented_game.getInitBoard()
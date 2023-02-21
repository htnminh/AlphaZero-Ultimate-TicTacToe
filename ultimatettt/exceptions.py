import numpy as np


class GameException(Exception):
    pass


class BoardWonException(GameException):
    def __init__(self, board_winner):
        if board_winner == 1:
            message = 'Player 1 already won, please start a new game' 
        elif board_winner == -1:
            message = 'Player 2 already won, please start a new game'
        else:
            message = 'The game was a draw, please start a new game'
        
        super().__init__(message)


class AreaWonException(GameException):
    def __init__(self, played_area, area_winner):
        if area_winner == 1:
            message = f'Local board {played_area} already won by player 1'
        elif area_winner == -1:
            message = f'Local board {played_area} already won by player 2'
        else:
            message = f'Local board {played_area} was a draw'
        super().__init__(message)


class AreaWrongException(GameException):
    def __init__(self, next_area, played_area):
        message = f'The next area is {next_area}, player is not allowed to play on {played_area}'
        super().__init__(message)
        

class CellPlayedException(GameException):
    def __init__(self, xyij, player):      
        if player == 1:
            message = f'Cell {xyij} is already played on by player 1'      
        elif player == -1:
            message = f'Cell {xyij} is already played on by player 2'  
        else:
            raise Exception(player)
        
        super().__init__(message)


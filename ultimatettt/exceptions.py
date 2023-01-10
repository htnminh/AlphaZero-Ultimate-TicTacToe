class GameException(Exception):
    pass


class BoardWonException(GameException):
    def __init__(self, board):
        message = f'Player {board} already won, please start a new game'    
        super().__init__(message)


class AreaWonException(GameException):
    def __init__(self, played_area):
        message = f'Area {played_area} already won'
        super().__init__(message)


class AreaWrongException(GameException):
    def __init__(self, next_area, played_area):
        message = f'The next area is {next_area}, player is not allowed to play on {played_area}'
        super().__init__(message)
        

class CellPlayedException(GameException):
    def __init__(self, xyij):      
        message = f'Cell {xyij} is already played'      
        super().__init__(message)


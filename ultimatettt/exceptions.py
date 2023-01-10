class BoardWonException(Exception):
    def __init__(self, board):
        message = f'Player {board} already won, please restart the game'    
        super().__init__(message)


class AreaWonException(Exception):
    def __init__(self, played_area):
        message = f'Area {played_area} already won'
        super().__init__(message)


class AreaWrongException(Exception):
    def __init__(self, next_area, played_area):
        message = f'The next area is {next_area}, player is not allowed to play on {played_area}'
        super().__init__(message)
        

class CellPlayedException(Exception):
    def __init__(self, xyij):      
        message = f'Cell {xyij} is already played'      
        super().__init__(message)


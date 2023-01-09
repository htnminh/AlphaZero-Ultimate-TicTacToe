import numpy as np


class Utils():
    def __init__(self):
        pass

    def check_win_array(self, array):
        # array == [1, 1, 1] or [2, 2, 2] -> 1 or 2 respectively, else 0
        first_entry = array[0]
        if np.all(array == first_entry) and first_entry != 0:
            return first_entry
        return 0

    def check_win_arrays(self, arrays):
        # if any of the arrays is won, return the winner
        return np.max(np.apply_along_axis(self.check_win_array, 1, arrays))
    
    def check_win_row_col(self, array):
        # check win for rows and cols of a 2d array
        return self.check_win_arrays(
            np.concatenate([*np.vsplit(array, 3), *np.vsplit(np.transpose(array), 3)])
        )

    def check_win_diagonal(self, array):
        # check win for two diagonals of a 2d array
        return self.check_win_arrays(
            np.stack([array.diagonal(), np.fliplr(array).diagonal()])
        )

    def check_win(self, array):
        # check win of a 2d array
        return self.check_win_row_col(array) or self.check_win_diagonal(array)



class Board():
    def __init__(self):
        # board entries:
        # 0: playable
        # 1: X (player 1)
        # 2: O (player 2)
        self.state_cell = np.zeros((3, 3, 3, 3), dtype=int)

        self.state_area = np.zeros((3, 3), dtype=int)
        self.state_board = 0

    
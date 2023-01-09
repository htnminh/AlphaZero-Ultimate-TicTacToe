import pprint

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

    def xyij_to_mn(self, xyij):
        # return a printable 2 dimensional index of a 4 dimensional index
        # denotes by (x, y, i, j) -> (m, n)
        x, y, i, j = xyij
        return 3*x+i, 3*y+j

    def mn_to_xyij(self, mn):
        # return a 4 dimensional index of a printable 2 dimensional index
        # denotes by (m, n) -> (x, y, i, j)
        m, n = mn
        return m // 3, n // 3, m % 3, n % 3

    def player_int_to_str(self, player_int, not_played_str, player_1_str, player_2_str):
        return not_played_str if player_int == 0 \
            else player_1_str if player_int == 1 \
            else player_2_str

    def cell_array_to_printable_array(self, array, not_played_str, player_1_str, player_2_str):
        # printable array of cell array
        str_array = np.full((9, 9), ' ', dtype=np.string_)
        for m in range(9):
            for n in range(9):
                x, y, i, j = self.mn_to_xyij((m, n))
                player_int = array[x, y, i, j]
                str_array[m, n] = self.player_int_to_str(
                    player_int, not_played_str, player_1_str, player_2_str)

        return str_array

    # TODO: cell_array_to_str
        

class State():
    def __init__(self):
        # board entries:
        # 0: playable/win-TBD
        # 1: X (player 1) played/won
        # 2: O (player 2) played/won

        # self.cell = np.zeros((3, 3, 3, 3), dtype=int)
        self.cell = np.zeros((3, 3, 3, 3))
        self.area = np.zeros((3, 3), dtype=int)
        self.board = 0

        self.last_area = None
        self.current_turn = 1

    def __str__(self):
        not_played_str = '-'
        player_1_str = 'X'
        player_2_str = 'O'

        # TODO: return cell_array_to_str of self.cell
        return pprint.pformat(Utils().cell_array_to_printable_array(
            self.cell, not_played_str, player_1_str, player_2_str))


# TODO: transfer to unittest
state = State()
state.cell[2, 2, 0, 0] = 1
state.cell[1, 1, 1, 1] = 2
state.cell[1, 0, 2, 2] = 1
print(state)

# TODO: ? CLI GAME ?
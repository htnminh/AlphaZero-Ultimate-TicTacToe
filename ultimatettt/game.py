import pprint

import numpy as np

from exceptions import \
    BoardWonException, AreaWonException, AreaWrongException, CellPlayedException

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
        # 0 -> ' ', 1 -> 'X', 2 -> 'O'
        return not_played_str if player_int == 0 \
            else player_1_str if player_int == 1 \
            else player_2_str

    def cell_array_to_printable_array(self, array, not_played_str, player_1_str, player_2_str):
        # printable array of cell array
        str_array = np.full((9, 9), ' ', dtype=str)
        for m in range(9):
            for n in range(9):
                x, y, i, j = self.mn_to_xyij((m, n))
                player_int = array[x, y, i, j]
                str_array[m, n] = self.player_int_to_str(
                    player_int, not_played_str, player_1_str, player_2_str)

        return str_array

    def cell_str_pformat(self, string):
        # a str of cell array to more beautiful one
        row_str_pformat = lambda row_str: row_str[0:3] + ' ' + row_str[3:6] + ' ' + row_str[6:9]
        cell_str = string.split('\n')
        cell_str = list(map(row_str_pformat, cell_str))
        return '\n'.join([*cell_str[0:3], '\n', *cell_str[3:6], '\n', *cell_str[6:9]])

    def cell_array_to_str(self, array, not_played_str, player_1_str, player_2_str):
        # cell array of state to str 
        str_array = self.cell_array_to_printable_array(array, not_played_str, player_1_str, player_2_str)
        row_to_str = lambda row: ''.join(row)
        str_array_row = np.apply_along_axis(row_to_str, 1, str_array)
        return self.cell_str_pformat('\n'.join(str_array_row))
        
        

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

        self.next_area = None
        self.next_player = 1

    def __str__(self):
        not_played_str = '-'
        player_1_str = 'X'
        player_2_str = 'O'

        seperator = '\n' + '=' * 35 + '\n'
        info_1 = f'board={self.board}\narea:\n{self.area}\n\ncell:\n'
        info_2 = f'\n\nnext_player={self.next_player}\nnext_area={self.next_area}'
        return seperator + info_1 + \
            Utils().cell_array_to_str(self.cell, not_played_str, player_1_str, player_2_str) + \
            info_2 + seperator

    def change_win_state(self, x, y, i, j):
        area_state = Utils().check_win(self.cell[x, y])
        if area_state != 0:
            self.area[x, y] = area_state
            self.board = Utils().check_win(self.area)

    def play(self, xyij):
        x, y, i, j = xyij

        if self.board != 0:
            raise BoardWonException(self.board)

        if self.area[x, y] != 0:
            raise AreaWonException((x, y))

        if self.next_area is not None and self.next_area != (x, y):
            raise AreaWrongException(self.next_area, (x, y))

        if self.cell[x, y, i, j] != 0:
            raise CellPlayedException(xyij)

        self.cell[x, y, i, j] = self.next_player
        self.change_win_state(x, y, i, j)
        self.next_player = 3 - self.next_player  # 2->1, 1->2
        if self.area[i, j] == 0:
            self.next_area = (i, j)
        else:
            self.next_area = None
            

def main():
    # TODO: transfer to test
    state = State()
    state.play((1,1,1,1))
    state.play((1,1,0,1))
    state.play((0,1,2,2))
    state.play((2,2,1,1))
    state.play((1,1,1,2))
    state.play((1,2,1,1))
    state.play((1,1,1,0))
    state.play((1,0,1,1))
    state.play((0,1,1,2))
    state.play((1,2,0,1))
    state.play((0,1,0,2))
    state.play((0,2,2,1))
    state.play((2,1,1,2))
    state.play((1,2,2,1))
    state.play((2,1,1,1))
    state.play((2,2,2,2))
    state.play((2,2,2,1))
    state.play((2,1,2,1))
    state.play((2,1,1,0))
    print(state, end='')

if __name__ == '__main__':
    main()


# TODO: ? CLI GAME ?
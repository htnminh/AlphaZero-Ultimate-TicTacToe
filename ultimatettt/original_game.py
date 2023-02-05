from typing import List

import numpy as np

from exceptions import (
    GameException,
    BoardWonException, AreaWonException,
    AreaWrongException, CellPlayedException)

class LogicUtils():
    def __init__(self):
        pass

    def check_win_array(self, array:np.ndarray) -> int:
        """
        Input:
            array -- an array of size (3, ), int/float entries in {-1, 0, 1, nan}

        Return:
            int -- if all entries are -1, 1, return that, else return 0

        Explain:
            Check an array if it is won, return -1 or 1 if won,
            since only one array cannot determine if it is a draw,
            therefore return 0.
        """
        first_entry = array[0]
        if np.all(array == first_entry) and first_entry != 0:
            return first_entry
        return 0

    def check_win_arrays(self, arrays:List[np.ndarray]) -> int:
        """
        Input:
            arrays -- list of arrays of size (3, ), int/float entries in {-1, 0, 1, nan}

        Return:
            int -- the winner (-1 or 1), else 0

        Explain:
            Only arrays cannot determine if it is a draw.
        """
        checked_array = np.apply_along_axis(self.check_win_array, 1, arrays)
        diff_from_0 = checked_array != 0
        if np.any(diff_from_0):
            return float(checked_array[diff_from_0][0])
        return 0

    
    def check_win_row_col(self, array:np.ndarray) -> int:
        """
        Input:
            array -- an array of size (3, 3), int/float entries in {-1, 0, 1, nan}

        Output:
            int -- return the winner for rows and columns (-1 or 1), else 0
        """
        return self.check_win_arrays(
            np.concatenate([*np.vsplit(array, 3), *np.vsplit(np.transpose(array), 3)])
        )

    def check_win_diagonal(self, array:np.ndarray) -> int:
        """
        Input:
            array -- an array of size (3, 3), int/float entries in {-1, 0, 1, nan}
        
        Output:
            int -- return the winner for two diagonals (-1 or 1), else 0
        """
        # check win for two diagonals of a 2d array
        return self.check_win_arrays(
            np.stack([array.diagonal(), np.fliplr(array).diagonal()])
        )

    def check_filled(self, array:np.ndarray) -> bool:
        """
        Input:
            array -- an array of size(3, 3), int/float entries in {-1, 0, 1, nan}

        Output:
            bool -- return if the array is filled with entries != 0

        Explain:
            0 indicates that the cell is not played, or an area is not determined
        """
        return True if np.all(array != 0) else False

    def check_win(self, array:np.ndarray) -> float:
        """
        Input:
            array -- an array of size(3, 3), int/float entries in {-1, 0, 1, nan}

        Output:
            float -- return the winner (-1 or 1), nan if draw, 0 if not determined
        """
        win_row_col = self.check_win_row_col(array)
        win_diagonal = self.check_win_diagonal(array)

        if win_row_col != 0:
            return win_row_col
        if win_diagonal != 0:
            return win_diagonal
        if self.check_filled(array):
            return np.nan
        return 0
           

    def xyij_to_mn(self, xyij):
        """return 2 dimensional index of a 4 dimensional index
        denotes by (x, y, i, j) -> (m, n)"""
        x, y, i, j = xyij
        return 3*x + i, 3*y + j

    def mn_to_xyij(self, mn):
        """return a 4 dimensional index of 2 dimensional index
        denotes by (m, n) -> (x, y, i, j)"""
        m, n = mn
        return m // 3, n // 3, m % 3, n % 3

    def k_to_xyij(self, k):
        area_number = k // 9
        index_in_area = k % 9
        return area_number // 3, area_number % 3, index_in_area // 3, index_in_area % 3

    def xyij_to_k(self, xyij):
        x, y, i, j = xyij
        area_number = 3*x + y
        index_in_area = 3*i + j
        return area_number*9 + index_in_area


    def cell_int_to_str(self, player_int:int, not_played_str, player_1_str, player_2_str):
        return not_played_str if player_int == 0 \
            else player_1_str if player_int == 1 \
            else player_2_str

    def cell_array_to_printable_array(self, array, not_played_str, player_1_str, player_2_str):
        """printable array of cell array"""
        str_array = np.full((9, 9), ' ', dtype=str)
        for m in range(9):
            for n in range(9):
                x, y, i, j = self.mn_to_xyij((m, n))
                player_int = array[x, y, i, j]
                str_array[m, n] = self.cell_int_to_str(
                    player_int, not_played_str, player_1_str, player_2_str)

        return str_array

    def cell_str_pformat(self, string):
        """a str of cell array to more beautiful one"""
        row_str_pformat = lambda row_str: row_str[0:3] + ' ' + row_str[3:6] + ' ' + row_str[6:9]
        cell_str = string.split('\n')
        cell_str = list(map(row_str_pformat, cell_str))
        return '\n'.join([*cell_str[0:3], '\n', *cell_str[3:6], '\n', *cell_str[6:9]])

    def cell_array_to_str(self, array, not_played_str, player_1_str, player_2_str):
        """cell array of state to str """
        str_array = self.cell_array_to_printable_array(array, not_played_str, player_1_str, player_2_str)
        row_to_str = lambda row: ''.join(row)
        str_array_row = np.apply_along_axis(row_to_str, 1, str_array)
        return self.cell_str_pformat('\n'.join(str_array_row))
        
        

class OriginalGame():

    def __init__(self):
        """
        cell_state entries:
            0: blank
            1: X (player 1) played
            -1: O (player 2) played
        
        area, board entries:
            0: not determined
            nan: draw
            1: X (player 1) won
            -1: O (player 2) won
        """
        self.cell_state = np.full((3, 3, 3, 3), 0, dtype=int)
        self.area = np.full((3, 3), 0, dtype=float)
        self.board = 0

        self.curr_area = None
        self.curr_player = 1


    def __str__(self):
        not_played_str = '-'
        player_1_str = 'X'
        player_2_str = 'O'

        seperator = '\n' + '=' * 35 + '\n'
        info_1 = f'board={self.board}\narea:\n{self.area}\n\ncell:\n'
        info_2 = f'\n\ncurr_player={self.curr_player}\ncurr_area={self.curr_area}'
        return seperator + info_1 + \
            LogicUtils().cell_array_to_str(self.cell_state, not_played_str, player_1_str, player_2_str) + \
            info_2 + seperator


    def update_area(self, xy):
        """
        Change self.area + change self.board
        """
        x, y = xy
        self.area[x, y] = LogicUtils().check_win(self.cell_state[x, y])

    def update_board(self):
        self.board = LogicUtils().check_win(self.area)
    
    def update_area_and_board(self, xy):
        self.update_area(xy)
        self.update_board()

    def update_all_areas_and_board(self):
        for x in range(3):
            for y in range(3):
                self.update_area((x, y))
        self.update_board()

    def check_playable_cell(self, xyij):
        """raise a corresponding exception if not playable"""
        x, y, i, j = xyij

        if not (self.board == 0):
            raise BoardWonException(self.board)

        if not (self.area[x, y] == 0):
            raise AreaWonException((x, y), self.area[x, y])

        if self.curr_area is not None and self.curr_area != (x, y):
            raise AreaWrongException(self.curr_area, (x, y))

        if self.cell_state[x, y, i, j] != 0:
            raise CellPlayedException(xyij, self.cell_state[x, y, i, j])


    def execute_move(self, xyij):
        x, y, i, j = xyij

        self.check_playable_cell(xyij)

        self.cell_state[x, y, i, j] = self.curr_player
        self.update_area_and_board((x, y))
        self.curr_player = -self.curr_player
        if self.area[i, j] == 0:
            self.curr_area = (i, j)
        else:
            self.curr_area = None
    

    def _reinit(self, cell_state, player, curr_area):
        self.cell_state = cell_state
        self.update_all_areas_and_board()
        self.curr_player = player
        self.curr_area = curr_area
        return self

    def _get_next_self(self, cell_state, player, xyij, curr_area):
        self._reinit(cell_state, player, curr_area)
        self.execute_move(xyij)
        return self

    def _get_valid_moves(self, cell_state, player, curr_area):
        """return a 4d array, 
        TODO: may need an improvement"""
        self._reinit(cell_state, player, curr_area)
        binary_4d_array = np.zeros((3, 3, 3, 3))
        for x in range(3):
            for y in range(3):
                for i in range(3):
                    for j in range(3):
                        try:
                            self.check_playable_cell((x, y, i, j))
                            binary_4d_array[x, y, i, j] = 1
                        except GameException:
                            pass
        return binary_4d_array

    def _get_game_ended(self, cell_state, player, curr_area):
        SMALL_VALUE = 1e-1
        """
        Board:
        0: not determined
        nan: draw
        1: X (player 1) won
        -1: O (player 2) won

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
        """
        self._reinit(cell_state, player, curr_area)
        if np.isnan(self.board):
            return SMALL_VALUE
        return self.board
        

def main():
    # TODO: transfer to test
    original_game = OriginalGame()
    original_game.execute_move((1,2,1,1))
    # print(state.cell_state)
    original_game.execute_move((1,1,0,1))
    original_game.execute_move((0,1,2,2))
    original_game.execute_move((2,2,1,1))
    original_game.execute_move((1,1,1,2))
    original_game.execute_move((1,2,1,0))
    original_game.execute_move((1,0,1,1))
    original_game.execute_move((1,1,1,1))
    original_game.execute_move((1,1,2,2))
    original_game.execute_move((2,2,1,2))
    original_game.execute_move((1,2,2,2))
    original_game.execute_move((2,2,1,0))
    original_game.execute_move((1,0,2,2))
    original_game.execute_move((1,1,2,1))
    original_game.execute_move((2,1,1,1))
    original_game.execute_move((0,0,1,1))
    original_game.execute_move((0,2,2,2))
    original_game.execute_move((0,0,2,2))
    original_game.execute_move((0,1,0,0))
    original_game.execute_move((0,0,0,0))
    print(original_game, end='')

if __name__ == '__main__':
    main()

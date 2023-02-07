import unittest

import numpy as np

from original_game import LogicUtils

class TestUtils(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.utils = LogicUtils()
    
    def test_check_win_array_1_won(self):
        self.assertEqual(self.utils.check_win_array(np.array([1, 1, 1])), 1)

    def test_check_win_array_2_won(self):
        self.assertEqual(self.utils.check_win_array(np.array([2, 2, 2])), 2)

    def test_check_win_array_0_full(self):
        self.assertEqual(self.utils.check_win_array(np.array([0, 0, 0])), 0)

    def test_check_win_array_not_equal_1st(self):
        self.assertEqual(self.utils.check_win_array(np.array([0, 1, 2])), 0)

    def test_check_win_array_not_equal_2nd(self):
        self.assertEqual(self.utils.check_win_array(np.array([1, 1, 0])), 0)


    def test_check_win_arrays_1_won(self):
        self.assertEqual(self.utils.check_win_arrays([
            np.array([0, 1, 2]),
            np.array([1, 1, 1]),
            np.array([0, 0, 2])
        ]), 1)

    def test_check_win_arrays_2_won(self):
        self.assertEqual(self.utils.check_win_arrays([
            np.array([2, 1, 0]),
            np.array([1, 0, 1]),
            np.array([2, 2, 2])
        ]), 2)

    def test_check_win_arrays_no_won_1st(self):
        self.assertEqual(self.utils.check_win_arrays([
            np.array([2, 1, 0]),
            np.array([1, 0, 1]),
            np.array([2, 1, 2])
        ]), 0)

    def test_check_win_arrays_no_won_2nd(self):
        self.assertEqual(self.utils.check_win_arrays([
            np.array([1, 1, 0]),
            np.array([1, 1, 2]),
            np.array([1, 1, 0])
        ]), 0)


    def test_check_win_row_col_1_won(self):
        self.assertEqual(self.utils.check_win_row_col(
            np.array([
                [1, 1, 0],
                [1, 1, 2],
                [2, 1, 2]
            ])
        ), 1)

    def test_check_win_row_col_2_won(self):
        self.assertEqual(self.utils.check_win_row_col(
            np.array([
                [1, 1, 0],
                [2, 2, 2],
                [2, 1, 2]
            ])
        ), 2)

    def test_check_win_row_col_no_won_1st(self):
        self.assertEqual(self.utils.check_win_row_col(
            np.array([
                [1, 1, 0],
                [2, 1, 2],
                [2, 0, 1]
            ])
        ), 0)

    def test_check_win_row_col_no_won_2nd(self):
        self.assertEqual(self.utils.check_win_row_col(
            np.array([
                [0, 1, 0],
                [0, 1, 0],
                [2, 0, 2]
            ])
        ), 0)

    
    def test_check_win_diagonal_1_won(self):
        self.assertEqual(self.utils.check_win_diagonal(
            np.array([
                [1, 1, 0],
                [0, 1, 0],
                [2, 0, 1]
            ])
        ), 1)

    def test_check_win_diagonal_2_won(self):
        self.assertEqual(self.utils.check_win_diagonal(
            np.array([
                [1, 1, 2],
                [0, 2, 0],
                [2, 0, 1]
            ])
        ), 2)

    def test_check_win_diagonal_no_won_1st(self):
        self.assertEqual(self.utils.check_win_diagonal(
            np.array([
                [1, 1, 1],
                [1, 2, 1],
                [1, 1, 1]
            ])
        ), 0)

    def test_check_win_diagonal_no_won_2nd(self):
        self.assertEqual(self.utils.check_win_diagonal(
            np.array([
                [1, 1, 0],
                [1, 0, 1],
                [0, 1, 1]
            ])
        ), 0)

    
    def test_check_win_1_won(self):
        self.assertEqual(self.utils.check_win(np.array([
            [0, 0, 2],
            [1, 1, 1],
            [2, 2, 1]
        ])), 1)

    def test_check_win_2_won(self):
        self.assertEqual(self.utils.check_win(np.array([
            [0, 0, 2],
            [1, 2, 1],
            [2, 2, 1]
        ])), 2)

    def test_check_win_no_won_1st(self):
        self.assertEqual(self.utils.check_win(np.array([
            [0, 0, 2],
            [1, 0, 1],
            [2, 2, 1]
        ])), 0)

    def test_check_win_no_won_2nd(self):
        self.assertEqual(self.utils.check_win(np.array([
            [1, 0, 1],
            [1, 2, 1],
            [2, 2, 0]
        ])), 0)

    # TODO: fix name
    def test_check_win_bug(self):
        self.assertEqual(self.utils.check_win(np.array([
            [0, 0, 2],
            [0, 0, 2],
            [0, 0, 1]
        ])), 0)

    # TODO
        

if __name__ == '__main__':
    unittest.main()
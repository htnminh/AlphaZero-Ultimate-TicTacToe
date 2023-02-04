from Game import Game
from original_game import LogicUtils, OriginalGame

import numpy as np


class ImplementationUtils():
    def __init__(self):
        pass

    def cell_state_4d_to_2d(self, cell_state):
        """
        this should be called as least as possible since it cost a quite amount of time,
        and other ways of implementing this isn't as obvious and not that better to be worth it

        Input:
            cell_state -- int array of size (3,3,3,3)

        Return:
            ndarray -- of size (9, 9)

        What it look like:
            original_game.cell_state = np.arange(81).reshape((3,3,3,3))  # testing only
            return ImplementationUtils().cell_state_to_2d(original_game.cell_state)

            [[ 0.  1.  2.  9. 10. 11. 18. 19. 20.]
            [ 3.  4.  5. 12. 13. 14. 21. 22. 23.]
            [ 6.  7.  8. 15. 16. 17. 24. 25. 26.]
            [27. 28. 29. 36. 37. 38. 45. 46. 47.]
            [30. 31. 32. 39. 40. 41. 48. 49. 50.]
            [33. 34. 35. 42. 43. 44. 51. 52. 53.]
            [54. 55. 56. 63. 64. 65. 72. 73. 74.]
            [57. 58. 59. 66. 67. 68. 75. 76. 77.]
            [60. 61. 62. 69. 70. 71. 78. 79. 80.]]
        """
        res = np.zeros((9, 9), dtype=float)
        logic_utils = LogicUtils()

        for x in range(3):
            for y in range(3):
                for i in range(3):
                    for j in range(3):
                        m, n = logic_utils.xyij_to_mn((x, y, i, j))
                        res[m, n] = cell_state[x, y, i, j]

        return res

    def cell_state_2d_to_4d(self, cell_state_2d):
        """the reverse operation of _4d_to_2d()"""
        res = np.zeros((3,3,3,3), dtype=float)
        logic_utils = LogicUtils()

        for m in range(9):
            for n in range(9):
                x, y, i, j = logic_utils.mn_to_xyij((m, n))
                res[x, y, i, j] = cell_state_2d[m, n]

        return res

class ImplementedGame(Game):
    def __init__(self):
        pass

    def getInitBoard(self):
        original_game = OriginalGame()
        return ImplementationUtils().cell_state_4d_to_2d(original_game.cell_state)

    def getBoardSize(self):
        return (9, 9)

    def getActionSize(self):
        return 81  # from 0 to 80
    
    def getNextState(self, board, player, action):
        return super().getNextState(board, player, action)



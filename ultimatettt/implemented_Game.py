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
            original_game.cell_state = np.arange(81).reshape((3,3,3,3))  # for testing only
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

    def cell_state_4d_to_1d(self, cell_state):
        res = np.zeros(81, dtype=float)
        logic_utils = LogicUtils()

        for x in range(3):
            for y in range(3):
                for i in range(3):
                    for j in range(3):
                        k = logic_utils.xyij_to_k((x, y, i, j))
                        res[k] = cell_state[x, y, i, j]

        return res

    def cell_state_1d_to_4d(self, cell_state_1d):
        res = np.zeros((3,3,3,3), dtype=float)
        logic_utils = LogicUtils()

        for k in range(81):
            x, y, i, j = logic_utils.k_to_xyij(k)
            res[x, y, i, j] = cell_state_1d[k]
        
        return res

class ImplementedGame(Game):
    """a board must always go with curr_area"""
    def __init__(self):
        pass

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
            curr_area
        """
        original_game = OriginalGame()

        startBoard = ImplementationUtils().cell_state_4d_to_2d(original_game.cell_state)
        return startBoard, original_game.curr_area

    def getBoardSize(self):
        return (9, 9)

    def getActionSize(self):
        return 81  # from 0 to 80
    
    def getNextState(self, board, player, action, curr_area):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
            curr_area
        """
        cell_state = ImplementationUtils().cell_state_2d_to_4d(board)
        xyij = LogicUtils().k_to_xyij(action)
        original_game = OriginalGame()._get_next_self(cell_state, player, xyij, curr_area)

        nextBoard = ImplementationUtils().cell_state_4d_to_2d(original_game.cell_state)
        return nextBoard, original_game.curr_player, original_game.curr_area
    
    def getValidMoves(self, board, player, curr_area):
        """
        Input:
            board: current board
            player: current player
            curr_area

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        cell_state = ImplementationUtils().cell_state_2d_to_4d(board)
        binary_4d_array = OriginalGame()._get_valid_moves(cell_state, player, curr_area)

        validMoves = ImplementationUtils().cell_state_4d_to_1d(binary_4d_array)
        return validMoves
    
    def getGameEnded(self, board, player, curr_area):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            curr_area

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
        """
        cell_state = ImplementationUtils().cell_state_2d_to_4d(board)

        r = OriginalGame()._get_game_ended(cell_state, player, curr_area)
        return r
    
    def getCanonicalForm(self, board, player, curr_area):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            curr_area

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
            curr_area
        """
        return board * player, curr_area
    
    def getSymmetries(self, board, pi, curr_area):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()
            curr_area

        Returns:
            symmForms: a list of [(board,pi, curr_area)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.

        TODO: improvements
        """
        cell_state_original = ImplementationUtils().cell_state_2d_to_4d(board)
        pi_4d_original = ImplementationUtils().cell_state_1d_to_4d(pi)
        if curr_area is not None:
            curr_area_tracker_original = np.zeros((3,3))
            curr_area_tracker_original[curr_area] = 1
        
        symmForms = list()

        for flip_big in [False, True]:
            for flip_small in [False, True]:
                for k_big in range(4):
                    for k_small in range(4):

                        # init
                        cell_state = cell_state_original.copy()
                        pi_4d = pi_4d_original.copy()
                        if curr_area is not None:
                            curr_area_tracker = curr_area_tracker_original.copy()

                        # flip big
                        if flip_big:
                            cell_state = np.flip(cell_state, axis=0)
                            pi_4d = np.flip(pi_4d, axis=0)
                            if curr_area is not None:
                                curr_area_tracker = np.flip(curr_area_tracker, axis=0)
                        
                        # flip small
                        if flip_small:
                            cell_state = np.flip(cell_state, axis=2)
                            pi_4d = np.flip(pi_4d, axis=2)
                        
                        # rotate
                        cell_state = np.rot90(cell_state, k=k_big, axes=(0, 1))
                        cell_state = np.rot90(cell_state, k=k_small, axes=(2, 3))

                        pi_4d = np.rot90(pi_4d, k=k_big, axes=(0, 1))
                        pi_4d = np.rot90(pi_4d, k=k_small, axes=(2, 3))

                        if curr_area is not None:
                            curr_area_tracker = np.rot90(curr_area_tracker, k=k_big, axes=(0, 1))
                            
                        # add result
                        symmForms.append(
                            (
                                ImplementationUtils().cell_state_4d_to_2d(cell_state),  # board
                                ImplementationUtils().cell_state_4d_to_1d(pi_4d),  # pi
                                None if curr_area is None \
                                    else tuple(np.argwhere(curr_area_tracker == 1).reshape(2))  # curr_area
                            )
                        )
        
        return symmForms

    def stringRepresentation(self, board:np.ndarray, curr_area):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        try:
            cell_state = ImplementationUtils().cell_state_2d_to_4d(board)
            cell_state_1d = ImplementationUtils().cell_state_4d_to_1d(cell_state)
            return str(cell_state_1d) + " " + str(curr_area)
        except:
            print(board)

    def get_mask_2d(self, board:np.ndarray, player, curr_area):
        '''simply a 2d array of valid moves'''
        cell_state = ImplementationUtils().cell_state_2d_to_4d(board)
        binary_4d_array = OriginalGame()._get_valid_moves(cell_state, player, curr_area)

        mask = ImplementationUtils().cell_state_4d_to_2d(binary_4d_array)
        return mask
    

if __name__ == '__main__':
    igame = ImplementedGame()
    next_board, next_player, next_curr_area = igame.getNextState(np.zeros((9, 9)), 1, 21, None)
    print(igame.get_mask_2d(next_board, next_player, next_curr_area))
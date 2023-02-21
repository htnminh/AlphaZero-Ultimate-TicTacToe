# human always play first in this version
import numpy as np

from implemented_Game import ImplementedGame, ImplementationUtils
from original_game import OriginalGame, LogicUtils
from implemented_NeuralNet import NNetWrapper
from utils import *

from Arena import Arena
from MCTS import MCTS

from main import args

def player_1(board, curr_area):
    cell_state = ImplementationUtils().cell_state_2d_to_4d(board)
    original_game = OriginalGame()._reinit(cell_state, 1, curr_area)
    
    print(original_game)
    inp = input('xyij=')
    x, y, i, j = map(int, [x for x in inp])
    
    k = LogicUtils().xyij_to_k((x, y, i, j))
    return k

game = ImplementedGame()
pnet = NNetWrapper(game)
pnet.load_checkpoint(
    folder=args.checkpoint,
    filename='checkpoint_10-ver_6.pth.tar'
)
board, curr_area = game.getInitBoard()

mcts = MCTS(game, pnet, args)

arena = Arena(
    # lambda x, y_curr_area: np.argmax(pmcts.getActionProb(x, y_curr_area, temp=0)),
    player_1,
    lambda x, y_curr_area: np.argmax(mcts.getActionProb(x, y_curr_area, temp=0)),
game)

arena.playGame()
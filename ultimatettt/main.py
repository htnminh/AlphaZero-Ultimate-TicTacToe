import logging

import coloredlogs

from Coach import Coach
from implemented_Game import ImplementedGame as Game
from implemented_NeuralNet import NNetWrapper as nn
from utils import *

from pprint import pprint
from implemented_NeuralNet import args as nn_args

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

args = dotdict({
    # 'numIters': 12,
    'numIters': 1,
    # 'numEps': 100,              # Number of complete self-play games to simulate during a new iteration.
    'numEps': 20,
    # 'tempThreshold': 15,        #
    'tempThreshold': 25,
    # 'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'updateThreshold': 0.55,
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    # 'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    # 'numMCTSSims': 20,   
    'numMCTSSims': 15,
    # 'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'arenaCompare': 24,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': True,
    'load_folder_file': ('/kaggle/input/ult-ttt-ver8-models', 'model_ver7_eg_ver8.tar'),
    'numItersForTrainExamplesHistory': 20,
})


def main():
    # My notes:
    pprint(args)
    pprint(nn_args)

    log.info('Loading %s...', Game.__name__)
    # g = Game(6)
    g = Game()

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()

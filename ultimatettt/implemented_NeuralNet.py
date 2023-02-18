import time
import os

import torch
import torch.optim as optim

from tqdm import tqdm

import numpy as np

from utils import *
from NeuralNet import NeuralNet
from UTTTNet import UTTTNet as Unnet

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    # 'epochs': 10,
    'epochs': 15,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),
    # 'num_channels': 512,
    'num_channels': 64,
    })

class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = Unnet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

        if args.cuda:
            self.nnet.cuda()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v) (+ curr_area) (+ mask_2d)
        """
        optimizer = optim.Adam(self.nnet.parameters())

        for epoch in range(args.epochs):
            print('EPOCH ::: ' + str(epoch + 1))
            self.nnet.train()
            pi_losses = AverageMeter()
            v_losses = AverageMeter()

            batch_count = int(len(examples) / args.batch_size)

            # t = tqdm(range(batch_count), desc='Training Net')
            # for _ in t:
            print('Training Net.....')
            print(f'batch_no: batch_count={batch_count}')
            for batch_no in range(batch_count):
                sample_ids = np.random.randint(len(examples), size=args.batch_size)
                boards, pis, vs, curr_areas, mask_2ds = list(zip(*[examples[i] for i in sample_ids]))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))
                mask_2ds = torch.FloatTensor(np.array(mask_2ds).astype(np.float64))
                # target_curr_areas = torch.FloatTensor(np.array(curr_areas).astype(np.float64))

                # predict
                if args.cuda:
                    # boards, target_pis, target_vs, curr_areas = \
                    boards, target_pis, target_vs, mask_2ds = \
                        boards.contiguous().cuda(), target_pis.contiguous().cuda(), \
                        target_vs.contiguous().cuda(), mask_2ds.contiguous().cuda()


                # compute output
                out_pi, out_v = self.nnet(torch.cat((boards, mask_2ds), 1))
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v

                # record loss
                pi_losses.update(l_pi.item(), boards.size(0))
                v_losses.update(l_v.item(), boards.size(0))
                # t.set_postfix(Loss_pi=pi_losses, Loss_v=v_losses)
                if batch_no == batch_count - 1:
                    print(f'Final batch info: Loss_pi={pi_losses}, Loss_v={v_losses}')

                # compute gradient and do SGD step
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

    def predict(self, board, mask_2d):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board = torch.FloatTensor(board.astype(np.float64))
        mask_2d = torch.FloatTensor(mask_2d.astype(np.float64))
        if args.cuda:
            board = board.contiguous().cuda()
            mask_2d = mask_2d.contiguous().cuda()
        board = board.view(1, self.board_x, self.board_y)
        self.nnet.eval()
        with torch.no_grad():
            pi, v = self.nnet(torch.cat((board, mask_2d.view(1, self.board_x, self.board_y)), 0))

        # print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    def loss_pi(self, targets, outputs):
        return -torch.sum(targets * outputs) / targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets - outputs.view(-1)) ** 2) / targets.size()[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        torch.save({
            'state_dict': self.nnet.state_dict(),
        }, filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise Exception("No model in path {}".format(filepath))
        map_location = None if args.cuda else 'cpu'
        checkpoint = torch.load(filepath, map_location=map_location)
        self.nnet.load_state_dict(checkpoint['state_dict'])

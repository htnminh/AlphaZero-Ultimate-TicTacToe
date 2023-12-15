import torch
import torch.nn as nn
import torch.nn.functional as F

from implemented_Game import Game


class UTTTNet(nn.Module):
    def __init__(self, game:Game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        super(UTTTNet, self).__init__()

        self.convA = nn.Conv2d(2, args.num_channels, 3, stride=3, padding=0, dilation=1)
        self.bn_convA = nn.BatchNorm2d(args.num_channels)

        self.convB = nn.Conv2d(2, args.num_channels, 3, stride=1, padding=0, dilation=3)
        self.bn_convB = nn.BatchNorm2d(args.num_channels)

        self.fcA1 = nn.Linear(args.num_channels*2*9, 1024)
        self.bn_fcA1 = nn.BatchNorm1d(1024)
        self.fcA2 = nn.Linear(1024, 512)
        self.bn_fcA2 = nn.BatchNorm1d(512)
        self.fcA3 = nn.Linear(512, self.action_size)
    
        self.fcB1 = nn.Linear(args.num_channels*2*9, 1024)
        self.bn_fcB1 = nn.BatchNorm1d(1024)
        self.fcB2 = nn.Linear(1024, 512)
        self.bn_fcB2 = nn.BatchNorm1d(512)
        self.fcB3 = nn.Linear(512, 1)

    def forward(self, s):  
        s = s.view(-1, 2, self.board_x, self.board_y)      

        a = F.relu(F.dropout2d(self.bn_convA(self.convA(s)), p=self.args.dropout, training=self.training))                     
        b = F.relu(F.dropout2d(self.bn_convB(self.convB(s)), p=self.args.dropout, training=self.training))                     

        s = torch.cat((a, b), 1)
        s = s.view(-1, self.args.num_channels*2*9)

        a = F.relu(F.dropout(self.bn_fcA1(self.fcA1(s)), p=self.args.dropout, training=self.training))
        b = F.relu(F.dropout(self.bn_fcB1(self.fcB1(s)), p=self.args.dropout, training=self.training))

        a = F.relu(F.dropout(self.bn_fcA2(self.fcA2(a)), p=self.args.dropout, training=self.training))
        b = F.relu(F.dropout(self.bn_fcB2(self.fcB2(b)), p=self.args.dropout, training=self.training))

        pi = self.fcA3(a)                                                                        
        v = self.fcB3(b)                                                                       

        return F.log_softmax(pi, dim=1), torch.tanh(v)



if __name__ == '__main__':
    import os

    from torchsummary import summary
    from implemented_Game import ImplementedGame
    from implemented_NeuralNet import args
    from torchview import draw_graph


    net = UTTTNet(ImplementedGame(), args)
    print(net)
    summary(net, ((2, 9, 9)))

    # this is runable on windows only
    os.environ["PATH"] += os.pathsep + './windows_10_msbuild_Release_graphviz-3.0.0-win32/Graphviz/bin'
    draw_graph(net, input_size=((args.batch_size, 2, 9, 9)), save_graph=True, filename='graph')
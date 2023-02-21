import torch

boards = torch.zeros((5, 1, 3, 3))  # batch_size x 1 x 9 x 9 
masks = torch.ones((5, 1, 3, 3)) # batch_size x 1 x 9 x 9 

inp = torch.cat((boards, masks), 1)
print(inp)
print(inp.size())   # batch_size x 2 x 9 x 9 
import numpy as np
import pprint

from game import Utils


a = [[None for _ in range(9)] for _ in range(9)]
for x in range(3):
    for y in range(3):
        for i in range(3):
            for j in range(3):
                m, n = Utils().xyij_to_mn((x, y, i, j))
                a[m][n] = f'{x}{y}{i}{j}'
pprint.pprint(a)

a = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
for m in range(9):
    for n in range(9):
        x, y, i, j = Utils().mn_to_xyij((m, n))
        a[x][y][i][j] = f'{m}{n}'
pprint.pprint(a)


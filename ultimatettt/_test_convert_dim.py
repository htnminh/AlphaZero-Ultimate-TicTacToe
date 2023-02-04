import numpy as np
import pprint

from original_game import LogicUtils
from implemented_Game import ImplementationUtils


a = np.arange(81).reshape(3,3,3,3)
print(a)

print('-' * 50)

# Test 4d <-> 2d
a_2d = ImplementationUtils().cell_state_4d_to_2d(a)
print(a_2d)
print(np.all(ImplementationUtils().cell_state_2d_to_4d(a_2d) == a))

print('-' * 50)

# Test 4d <-> 1d
a_1d = np.zeros(81)
for k in range(81):
    x, y, i, j = LogicUtils().k_to_xyij(k)
    a_1d[k] = a[x, y, i, j]
print(a_1d)

a_generate = np.zeros((3,3,3,3))
for x in range(3):
    for y in range(3):
        for i in range(3):
            for j in range(3):
                k = LogicUtils().xyij_to_k((x, y, i, j))
                a_generate[x, y, i, j] = a_1d[k]
print(np.all(a_generate == a))
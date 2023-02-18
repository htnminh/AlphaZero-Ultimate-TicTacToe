import numpy as np
import pprint

from original_game import LogicUtils
from implemented_Game import ImplementationUtils


a = np.arange(81).reshape(3,3,3,3)
print(a)

print('-' * 50)

# 4d <-> 2d
a_2d = ImplementationUtils().cell_state_4d_to_2d(a)
print(a_2d)
print(np.all(ImplementationUtils().cell_state_2d_to_4d(a_2d) == a))

print('-' * 50)

# 4d <-> 1d
a_1d = ImplementationUtils().cell_state_4d_to_1d(a)
print(a_1d)
print(np.all(ImplementationUtils().cell_state_1d_to_4d(a_1d) == a))
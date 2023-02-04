import numpy as np
from implemented_Game import ImplementationUtils

# 

a = np.arange(81).reshape(3,3,3,3)
print(ImplementationUtils().cell_state_4d_to_2d(a))

print('-' * 50)

a_rotated = np.rot90(a)
print(ImplementationUtils().cell_state_4d_to_2d(a_rotated))

print('-' * 20)

a_rotated = np.rot90(a_rotated)
print(ImplementationUtils().cell_state_4d_to_2d(a_rotated))

print('-' * 20)

a_rotated = np.rot90(a_rotated)
print(ImplementationUtils().cell_state_4d_to_2d(a_rotated))

print('-' * 20)

# 
print('-' * 50)

a = np.arange(81).reshape(3,3,3,3)
print(ImplementationUtils().cell_state_4d_to_2d(a))

print('-' * 50)

a_rotated = np.rot90(a, axes=(2, 3))
print(ImplementationUtils().cell_state_4d_to_2d(a_rotated))

print('-' * 20)

a_rotated = np.rot90(a_rotated, axes=(2, 3))
print(ImplementationUtils().cell_state_4d_to_2d(a_rotated))

print('-' * 20)

a_rotated = np.rot90(a_rotated, axes=(2, 3))
print(ImplementationUtils().cell_state_4d_to_2d(a_rotated))

print('-' * 20)

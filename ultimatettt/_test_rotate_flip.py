import numpy as np
from implemented_Game import ImplementationUtils
from copy import deepcopy

import pprint

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

# 
print('-' * 50)

a_curr_area_tracker = np.zeros((3,3))
curr_area = (1,2)
a_curr_area_tracker[curr_area] = 1
print(a_curr_area_tracker)
print(curr_area)

a_curr_area_tracker = np.rot90(a_curr_area_tracker)
curr_area = np.argwhere(a_curr_area_tracker == 1)
print(a_curr_area_tracker)
print(tuple(curr_area.reshape(2)))


# only choose axis=0 or 1, and 2 or 3
# so 0 and 2
print('-' * 50)

counter = 0
symms = set()
a_test_flip_rot90_original = np.arange(81).reshape(3,3,3,3)

for flip_big in [False, True]:
    for flip_small in [False, True]:
        for k_big in range(4):
            for k_small in range(4):

                a_test_flip_rot90 = a_test_flip_rot90_original.copy()
            
                if flip_big:
                    a_test_flip_rot90 = np.flip(a_test_flip_rot90, axis=0)
                if flip_small:
                    a_test_flip_rot90 = np.flip(a_test_flip_rot90, axis=2)

                a_test_flip_rot90 = np.rot90(a_test_flip_rot90, axes=(0, 1), k=k_big)
                a_test_flip_rot90 = np.rot90(a_test_flip_rot90, axes=(2, 3), k=k_small)

                counter += 1
                symms.add(tuple(a_test_flip_rot90.flatten()))
                # print(a_test_flip_rot90)
    
print(counter, len(symms))
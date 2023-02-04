from game import Utils
import numpy as np

a = Utils().check_win_array([np.nan, np.nan, np.nan])
print(np.nan == np.nan)
print(a)
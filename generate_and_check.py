import sys
import numpy as np
import pandas as pd
from generation import generate_data
from lag_searching_methods import corrmatrix_var_min, corrmatrix_cor_max

filenum = int(sys.argv[1])

n_row = 300
n_col = 3
n_prin_var = 2

mean_prin_var = 0
sd_prin_var = 1
lag_interval = (5, 25)
coefs_interval = (1, 2)

h = 40
max_lag = 30

data = generate_data(n_row, n_col, n_prin_var,
                     mean_prin_var, sd_prin_var,
                     lag_interval, coefs_interval)
default_corrmatrix = np.corrcoef(data, rowvar=False)
sh_corrmatrix = corrmatrix_var_min(data, h, max_lag)
max_corrmatrix = corrmatrix_cor_max(data, max_lag)

def_svd = np.linalg.svd(default_corrmatrix)
sh_svd = np.linalg.svd(sh_corrmatrix)
max_svd = np.linalg.svd(max_corrmatrix)

def_df = pd.DataFrame(def_svd[1])
def_df.to_csv("results/default/singular_values_{}.csv".format(filenum), index=None, header=None)
sh_df = pd.DataFrame(sh_svd[1])
sh_df.to_csv("results/shifted/singular_values_{}.csv".format(filenum), index=None, header=None)
max_df = pd.DataFrame(max_svd[1])
max_df.to_csv("results/max_cor/singular_values_{}.csv".format(filenum), index=None, header=None)

import numpy as np


def generate_data(n_row, n_col,
                  n_prin_var,
                  mean_prin_var=0,
                  sd_prin_var=1,
                  lag_interval=(5, 15),
                  coefs_interval=(1, 2)):

    # Генерирует набор данных в виде numpy матрицы.
    # n_row - количество строк полученных данных,
    # n_col - количество столбцов (переменных),
    # n_prin_var - количество объясняющих переменных.

    n_row_prin_var = n_row + lag_interval[1]
    principal_variables = np.zeros((n_row_prin_var, n_prin_var))
    for i in range(0, n_prin_var):
        principal_variables[:, i] = np.random.normal(mean_prin_var, sd_prin_var, n_row_prin_var)

    coefs = np.random.uniform(coefs_interval[0], coefs_interval[1], (n_col, n_prin_var))
    lags = np.random.randint(lag_interval[0], lag_interval[1], (n_col, n_prin_var))
    data = np.zeros((n_row, n_col))

    for i in range(0, n_col):
        new_var = np.zeros(n_row)
        for j in range(0, n_prin_var):
            start = lag_interval[1] - lags[i, j]
            new_var += coefs[i, j] * principal_variables[start:start+n_row, j]
        data[:, i] = new_var

    return data



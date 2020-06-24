import numpy as np


def corcoef_with_lag(x, y, lag, reverse_order=False):
    # Вычисляет коэффициент корреляции с фиксированным сдвигом, в заданном порядке.

    if reverse_order:
        coef = np.corrcoef(y[:-lag or None], x[lag:])[0, 1]
    else:
        coef = np.corrcoef(x[:-lag or None], y[lag:])[0, 1]

    return coef


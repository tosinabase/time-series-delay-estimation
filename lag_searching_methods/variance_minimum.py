import numpy as np


def slice_corcoefs(x, y, h, s):
    # Возвращает массив коэффициентов корреляции,
    # последовательно посчитанных на срезах массивов x и y, где
    # s - велечина сдвига срезов относительно друг друга,
    # h - размер среза.
    res = [np.corrcoef(x[i: i + h], y[i + s: i + h + s])[0, 1] for i in range(0, len(x) - h - s + 1)]
    return res


def lag_var_min_current_order(x, y, h, max_lag):
    # Вычисляет лаг для массивов x и y,
    # соответствующий минимальной дисперсии корреляций.
    # Только в заданном порядке!
    v_min = np.var(slice_corcoefs(x, y, h, 0))
    i = 0
    for lag in range(1, max_lag + 1):
        v = np.var(slice_corcoefs(x, y, h, lag))
        if v < v_min:
            v_min = v
            i = lag

    res_lag = i
    return res_lag


def lag_with_variance_minimum(x, y, h, max_lag):
    # Вычисляет лаг для массивов x и y,
    # соответствующий минимальной дисперсии корреляций.

    # Возвращает пару (res_lag, reverse_order), где reverse_order имеет булево значение,
    # показывающее порядок массивов x и y, при котором достигается минимум дисперсии.
    # Если reverse_order == True, то это значит, что оптимальный лаг res_lag достигается
    # в обратном порядке массивов x, y.
    v_min = np.var(slice_corcoefs(x, y, h, 0))
    u_min = np.var(slice_corcoefs(y, x, h, 0))
    i = 0
    j = 0
    for lag in range(1, max_lag + 1):
        v = np.var(slice_corcoefs(x, y, h, lag))
        u = np.var(slice_corcoefs(y, x, h, lag))
        if v < v_min:
            v_min = v
            i = lag
        if u < u_min:
            u_min = u
            j = lag
    if v_min < u_min:
        res_lag = i
        reverse_order = False
    else:
        res_lag = j
        reverse_order = True

    return res_lag, reverse_order


def corrcoef_with_variance_minimum(x, y, h, max_lag):
    # Вычисляет коэффициент корреляции для массивов x и y,
    # соответствующий минимальной дисперсии корреляций.

    v_min = np.var(slice_corcoefs(x, y, h, 0))
    u_min = np.var(slice_corcoefs(y, x, h, 0))
    i = 0
    j = 0
    for lag in range(1, max_lag + 1):
        v = np.var(slice_corcoefs(x, y, h, lag))
        u = np.var(slice_corcoefs(y, x, h, lag))
        if v < v_min:
            v_min = v
            i = lag
        if u < u_min:
            u_min = u
            j = lag
    if v_min <= u_min:
        coef = np.corrcoef(x[:-i or None], y[i:])[0, 1]
    else:
        coef = np.corrcoef(y[:-j or None], x[j:])[0, 1]
    return coef


def corrmatrix_var_min(data, h, max_lag):
    # Вычисляет матрицу корреляций с учетом лагов
    # в соответствии с методом минимума дисперсий
    # коэффициентов корреляции.
    n_col = data.shape[1]
    corrmatrix = np.zeros((n_col, n_col))
    for i in range(0, n_col):
        for j in range(0, n_col):
            if i < j:
                x = data[:, i]
                y = data[:, j]
                corr = corrcoef_with_variance_minimum(x, y, h, max_lag)
                corrmatrix[i, j] = corr
                corrmatrix[j, i] = corr

        corrmatrix[i, i] = 1

    return corrmatrix


# Usage Example:
if __name__ == '__main__':
    a = np.random.normal(0, 1, 300)
    b = a + 2 * np.random.normal(0, 0.5, 300)
    print('Истинное значение корреляции:', np.corrcoef(a, b)[0, 1])

    x = np.concatenate((a, np.random.uniform(0, 5, 21)))
    y = np.concatenate((np.random.uniform(0, 5, 21), b))
    print('Коэффициент корреляции для сдвинутых переменных:', np.corrcoef(x, y)[0, 1])

    lag = lag_var_min_current_order(x, y, 40, 30)
    print(lag)

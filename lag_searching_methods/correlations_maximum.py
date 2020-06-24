import numpy as np


def lag_and_coef_with_cor_max(x, y, max_lag):
    # Возвращает лаг и коэффициент корреляции для массивов x и y,
    # соответствующий максимуму корреляций.

    coefs = [np.corrcoef(x, y)[0, 1]]
    coefs.extend(
        [np.corrcoef(x[:-lag], y[lag:])[0, 1]
         for lag in range(1, max_lag + 1)]
    )

    res_lag = np.argmax(coefs)
    corr = coefs[res_lag]

    return res_lag, corr


def corrmatrix_cor_max(data, max_lag):
    # Вычисляет матрицу корреляций с учетом лагов
    # в соответствии с методом максимумов корреляций
    n_col = data.shape[1]
    corrmatrix = np.zeros((n_col, n_col))
    for i in range(0, n_col):
        for j in range(0, n_col):
            if i < j:
                x = data[:, i]
                y = data[:, j]
                _, corr = lag_and_coef_with_cor_max(x, y, max_lag)
                _, rev_corr = lag_and_coef_with_cor_max(y, x, max_lag)

                if rev_corr > corr:
                    corr = rev_corr

                corrmatrix[i, j] = corr
                corrmatrix[j, i] = corr

        corrmatrix[i, i] = 1

    return corrmatrix


# Пример:
if __name__ == '__main__':
    input_lag = 21

    a = np.random.normal(0, 1, 300)
    b = 3 * a + 5

    x = np.concatenate((a, [0] * input_lag))
    y = np.concatenate(([0] * input_lag, b))

    lag, cor = lag_and_coef_with_cor_max(x, y, 30)

    report = f'''
    Истинный лаг: {input_lag}
    Лаг, найденный методом максимумов корреляций {lag}
    '''
    print(report)


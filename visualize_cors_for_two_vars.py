import numpy as np
import matplotlib.pyplot as plt
from numpy.random.mtrand import _rand as global_randstate

from lag_searching_methods import slice_corcoefs, lag_with_variance_minimum, corcoef_with_lag


output_folder = 'results/'
input_lag = 21
global_randstate.seed(965)


a = np.random.normal(0, 1, 500)
b = 3*a + 2 * np.random.normal(0, 1, 500)
cor_default = np.corrcoef(a, b)[0, 1]

ab_cors = slice_corcoefs(a, b, 40, 0)
plt.scatter(range(len(ab_cors)), ab_cors)
plt.ylim(-1, 1)
plt.savefig(output_folder + 'default_cors.png')
plt.close()

x = np.concatenate((a, np.random.uniform(0, 5, input_lag)))
y = np.concatenate((np.random.uniform(0, 5, input_lag), b))
cor_shifted = np.corrcoef(x, y)[0, 1]

xy_cors = slice_corcoefs(x, y, 40, 0)
plt.scatter(range(len(xy_cors)), xy_cors)
plt.ylim(-1, 1)
plt.savefig(output_folder + 'cors_shifted_vars.png')
plt.close()

lag, rev_ord = lag_with_variance_minimum(x, y, 40, 30)
cor_min_var = corcoef_with_lag(x, y, lag, rev_ord)

xy_cors_min_var = slice_corcoefs(x, y, 40, lag)
plt.scatter(range(len(xy_cors_min_var)), xy_cors_min_var)
plt.ylim(-1, 1)
plt.savefig(output_folder + 'cors_with_optimal_lag.png')
plt.close()

params = {'input_lag': input_lag,
          'true_cor': cor_default,
          'true_var': np.var(ab_cors),
          'false_cor': cor_shifted,
          'false_lag': 0,
          'false_var': np.var(xy_cors),
          'founded_cor': cor_min_var,
          'founded_lag': lag,
          'founded_var': np.var(xy_cors_min_var)}

report = '''
Истинный Лаг = {input_lag}

Истинные показатели:
Коэффициент корреляции = {true_cor}
Лаг, с которым посчитан коэффициент корреляции = 0
Дисперсия = {true_var}

До нахождения оптимального лага:
Коэффициент корреляции = {false_cor}
Лаг, с которым посчитан коэффициент корреляции = {false_lag}
Дисперсия = {false_var}

После нахождения оптимального лага:
Коэффициент корреляции = {founded_cor}
Лаг, с которым посчитан коэффициент корреляции = {founded_lag}
Дисперсия = {founded_var}
'''

report = report.format(**params)
tex_report = r'''
    \hline
    Параметр & Истинные значения & Без учета лага & После применения метода \\ \hline
    Корреляция & {true_cor:.4f} & {false_cor:.4f} & {founded_cor:.4f} \\ \hline
    Лаг & {input_lag} & 0 & {founded_lag}   \\ \hline
    Дисперсия &  {true_var:.4f} & {false_var:.4f} & {founded_var:.4f} \\
    \hline
'''

tex_report = tex_report.format(**params)

print(report)
print(tex_report)

import json
import os
import numpy as np
import pandas as pd
from multiprocessing import Pool
from sklearn.metrics import mean_squared_error, mean_absolute_error

from efficiency_comparison import Generator
from lag_searching_methods import \
    lag_var_min_current_order, lag_and_coef_with_cor_max


class Checker:
    generator = None
    max_lag = None
    h = None
    max_cor_result = None
    min_var_result = None
    results = None
    report = None

    def __init__(self, generator, max_lag=30, h=40):
        self.generator = generator
        self.max_lag = max_lag
        self.h = h

    def max_cor_for_array(self, data):
        result = [lag_and_coef_with_cor_max(x, y, self.max_lag)[0] for x, y in data]
        return result

    def var_min_for_array(self, data):
        result = [lag_var_min_current_order(x, y, self.h, self.max_lag) for x, y in data]
        return result

    @staticmethod
    def check_method(data, method):
        n_parts = os.cpu_count()
        parts = [part.tolist() for part in np.array_split(data, n_parts)]

        pool = Pool(n_parts)
        result_parts = pool.map(method, parts)

        result = []
        for part in result_parts:
            result.extend(part)

        pool.close()

        return result

    def max_corr_by_data(self, data):
        result = self.check_method(data, self.max_cor_for_array)
        return result

    def min_var_by_data(self, data):
        result = self.check_method(data, self.var_min_for_array)
        return result

    def check_max_cor(self):
        self.max_cor_result = {'real': self.generator.real_lags}
        for name in self.generator.data:
            result = self.max_corr_by_data(self.generator.data[name])
            self.max_cor_result[name] = result

    def check_min_var(self):
        self.min_var_result = {'real': self.generator.real_lags}
        for name in self.generator.data:
            result = self.min_var_by_data(self.generator.data[name])
            self.min_var_result[name] = result

    def check_all(self):
        self.check_max_cor()
        self.check_min_var()

        return self.report_all()

    @staticmethod
    def make_report(result):
        df = pd.DataFrame(result)
        report = {'accuracy': {},
                  'ME': {},
                  'RMSE': {},
                  'MAE': {},
                  'std': {}}

        for col in df.drop('real', axis=1).columns:
            report['accuracy'][col] = (df[col] == df['real']).sum() / len(df)
            report['ME'][col] = (df['real'] - df[col]).mean()
            report['RMSE'][col] = mean_squared_error(df['real'], df[col], squared=False)
            report['MAE'][col] = mean_absolute_error(df['real'], df[col])
            report['std'][col] = (df['real'] - df[col]).std()

        return df, report

    def report_all(self):
        self.report = {}
        self.results = {}
        for result, method_name in [(self.max_cor_result, 'max_cor'),
                                    (self.min_var_result, 'min_var')]:
            df, method_report = self.make_report(result)
            self.results[method_name] = df
            self.report[method_name] = method_report

        print(json.dumps(self.report, indent=10))
        return self.results, self.report


if __name__ == '__main__':
    from time import time
    gen = Generator(total_num=100)
    gen.generate_linear_case()

    ch = Checker(gen)
    print('started')
    start = time()
    ch.check_min_var()
    print(time() - start)

    print('Success')

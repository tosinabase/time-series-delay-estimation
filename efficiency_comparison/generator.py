import numpy as np

from efficiency_comparison.utils import linear_function, parabolic_function, hyperbolic_function


class Generator:
    real_lags = None
    kernel = None

    total_num = None
    size = None
    kernel_mean = None
    kernel_std = None
    noise_part = 0.1

    data = None

    def __init__(self, total_num, vector_size=300,
                 min_lag=5, max_lag=25,
                 noise_part=0.1,
                 mode='stationary',
                 **kwargs):
        # total_num - количество испытаний,
        # vector_length - длина каждого вектора,
        # min_lag - минимальный лаг для генерирования,
        # max_lag - максимальный лаг для генерирования.
        # mode = 'stationary' or 'random-walk'

        # mean=0, std=1,
        # start_point
        # dist

        self.total_num = total_num
        self.size = vector_size
        self.noise_part = noise_part
        self.data = {}

        self.real_lags = np.random.randint(min_lag, max_lag, total_num)
        self.generate_kernel(mode, **kwargs)

    def generate_kernel(self, mode, **kwargs):
        if mode == 'stationary':

            self.kernel_mean = kwargs.get('mean', 0)
            self.kernel_std = kwargs.get('std', 1)

            self.kernel = [np.random.normal(self.kernel_mean,
                                            self.kernel_std,
                                            lag + self.size)
                           for lag in self.real_lags]

        elif mode == 'random-walk':
            start_point = kwargs.get('start_point', 1)
            distribution = kwargs.get('dist', 'normal')
            mean = kwargs.get('mean', 0)
            std = kwargs.get('std', 1)
            low = kwargs.get('low', -1)
            high = kwargs.get('high', 1)

            if distribution == 'normal':
                self.kernel = [np.concatenate(
                                    [np.array([start_point]),
                                     np.random.normal(mean, std, lag + self.size)]
                                              ).cumsum()
                               for lag in self.real_lags]

            elif distribution == 'uniform':
                self.kernel = [np.concatenate(
                                    [np.array([start_point]),
                                     np.random.uniform(low, high, lag + self.size)]
                                              ).cumsum()
                               for lag in self.real_lags]

            else:
                raise Exception("Unexpected parameter: distribution. "
                                "Use 'normal or 'uniform'.")

        else:
            raise Exception("Unexpected mode. "
                            "Use 'stationary' or 'random-walk'.")

    def generate_by_function(self, func, name, noise_part=None, **kwargs):
        # y = func(x) + noise
        if noise_part is None:
            noise_part = self.noise_part

        ys = [func(x, **kwargs) for x in self.kernel]

        # add noise
        ys = [y + np.random.normal(0, noise_part * np.std(y), len(y))
              for y in ys]

        data = [(x[lag:], y[:-lag])
                for x, y, lag in zip(self.kernel, ys, self.real_lags)]
        self.data[name] = data

    def generate_linear_case(self, a=1, c=0, noise_part=None):
        # y = a*x + c + noise
        self.generate_by_function(linear_function, 'linear', noise_part, a=a, c=c)

    def generate_parabolic_case(self, a=1, b=1, c=0, noise_part=None):
        # y = a*x^2 + b*x + c + noise
        self.generate_by_function(parabolic_function, 'parabolic', noise_part, a=a, b=b, c=c)

    def generate_hyperbolic_case(self, a=1, c=0, noise_part=None):
        # y = a/x + c + noise
        self.generate_by_function(hyperbolic_function, 'hyperbolic', noise_part, a=a, c=c)


if __name__ == '__main__':
    gen = Generator(total_num=1000, mode='random-walk', start_point=10.)
    gen.generate_hyperbolic_case(a=1, c=4)
    gen.generate_by_function(np.exp, 'e^x')
    gen.generate_linear_case()
    print('Success')



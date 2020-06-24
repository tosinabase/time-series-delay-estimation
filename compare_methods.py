import numpy as np
import pandas as pd
from time import time

from efficiency_comparison import Checker, Generator


def generate(gen):
    gen.generate_linear_case(a=2, c=5)
    gen.generate_parabolic_case(a=15, b=0, c=4)
    gen.generate_hyperbolic_case(a=1, c=4)

    gen.generate_by_function(lambda x: 1 / x ** 2, '1/x^2')
    gen.generate_by_function(np.exp, 'e^x')
    gen.generate_by_function(lambda x: np.exp(-x), 'e^(-x)')
    gen.generate_by_function(lambda x: np.exp(-x ** 2), 'e^(-x^2)')
    gen.generate_by_function(np.sin, 'sin')
    gen.generate_by_function(np.cos, 'cos')


number = 1000
gen_rw = Generator(total_num=number, noise_part=0.1,
                   mode='random-walk',
                   start_point=10., std=0.5)
gen_st = Generator(total_num=number, noise_part=0.1,
                   mean=3.5, std=1,
                   mode='stationary')

generate(gen_rw)
generate(gen_st)

ch_rw = Checker(gen_rw)
start = time()
dfs_rw, report_rw = ch_rw.check_all()
print(time() - start)

ch_st = Checker(gen_st)
start = time()
dfs_st, report_st = ch_st.check_all()
print(time() - start)



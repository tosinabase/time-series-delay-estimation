import pandas as pd


def calc_mq(df):
    return (df['s0'] + df['s1']) / (df['s0'] + df['s1'] + df['s2'])


default_df = pd.read_csv("results/default_df.csv")
shifted_df = pd.read_csv("results/shifted_df.csv")
max_cor_df = pd.read_csv("results/max_cor_df.csv")

default_df['ma'] = calc_mq(default_df)
shifted_df['ma'] = calc_mq(shifted_df)
max_cor_df['ma'] = calc_mq(max_cor_df)

def_percentage = (default_df['ma'] >= 0.75).sum() / len(default_df) * 100
min_var_percentage = (shifted_df['ma'] >= 0.75).sum() / len(shifted_df) * 100
max_cor_percentage = (max_cor_df['ma'] >= 0.75).sum() / len(max_cor_df) * 100

report = f'''
results:
default corrmatrix = {def_percentage}
min var corrmatrix = {min_var_percentage}
max cor corrmatrix = {max_cor_percentage}
'''

print(report)

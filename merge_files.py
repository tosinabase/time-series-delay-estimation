import numpy as np
import pandas as pd

default_df = pd.DataFrame(columns=['s0', 's1', 's2'])
shifted_df = pd.DataFrame(columns=['s0', 's1', 's2'])
max_cor_df = pd.DataFrame(columns=['s0', 's1', 's2'])

for i in range(0, 10000):
    default_row = pd.read_csv("results/default/singular_values_{}.csv".format(i), header=None)
    default_row = default_row.transpose()
    default_row.rename(columns={0: 's0', 1: 's1', 2: 's2'}, index={0: i}, inplace=True)
    default_df = pd.concat([default_df, default_row], sort=False)

    shifted_row = pd.read_csv("results/shifted/singular_values_{}.csv".format(i), header=None)
    shifted_row = shifted_row.transpose()
    shifted_row.rename(columns={0: 's0', 1: 's1', 2: 's2'}, index={0: i}, inplace=True)
    shifted_df = pd.concat([shifted_df, shifted_row], sort=False)

    max_cor_row = pd.read_csv("results/max_cor/singular_values_{}.csv".format(i), header=None)
    max_cor_row = max_cor_row.transpose()
    max_cor_row.rename(columns={0: 's0', 1: 's1', 2: 's2'}, index={0: i}, inplace=True)
    max_cor_df = pd.concat([max_cor_df, max_cor_row], sort=False)

default_df.to_csv("results/default_df.csv", index=None)
shifted_df.to_csv("results/shifted_df.csv", index=None)
max_cor_df.to_csv("results/max_cor_df.csv", index=None)


deflt = pd.DataFrame()
shft = pd.DataFrame()
max_cor = pd.DataFrame()

deflt['x'] = default_df['s0']/default_df['s1']
deflt['y'] = default_df['s1']/default_df['s2']

shft['x'] = shifted_df['s0']/shifted_df['s1']
shft['y'] = shifted_df['s1']/shifted_df['s2']

max_cor['x'] = max_cor_df['s0']/max_cor_df['s1']
max_cor['y'] = max_cor_df['s1']/max_cor_df['s2']

deflt.to_csv("results/default_relations.csv", index=None)
shft.to_csv("results/shifted_relations.csv", index=None)
max_cor.to_csv("results/max_cor_relations.csv", index=None)

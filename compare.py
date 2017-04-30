import pandas as pd
import numpy as np
import operator

def equally_weighted_portfolio(returns, k):
    return np.sum(returns.iloc[k,:])/num_stocks


eq_returns = []
CW = 1
for k in range(BACKUP,num_rows):
    CW = CW * (1+equally_weighted_portfolio(returns,k)/100)
    eq_returns.append(CW)


def get_cumulative_wealth():
    cw = 1
    for i in range(len(eq_returns)):
        cw *= (1+eq_returns[i]/100)
    return cw

nn = pd.DataFrame()
nn['bandit'] = realized_return_list
nn['equal'] = eq_returns
nn['diff=bandit-equal'] = map(operator.sub,realized_return_list,eq_returns)
nn.to_csv('results{}.csv'.format(LAG), index=False)
#cw2 = get_cumulative_wealth()

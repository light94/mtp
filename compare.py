import pandas as pd
import numpy as np
import operator

def equally_weighted_portfolio(returns, k):
    return np.sum(returns.iloc[k,:])/num_stocks


eq_returns = []
eq_cum_wealth = []
CW = 1
for k in range(BACKUP,num_rows):
    realized_return = equally_weighted_portfolio(returns,k) 
    CW = CW * (1+realized_return/100)
    eq_returns.append(realized_return)
    eq_cum_wealth.append(CW)


def get_cumulative_wealth():
    cw = 1
    for i in range(len(eq_returns)):
        cw *= (1+eq_returns[i]/100)
    return cw

nn = pd.DataFrame()
nn['bandit_return'] = realized_return_list
nn['equal_returns'] = eq_returns
nn['bandit_cum_wealth'] = cumulative_wealth_list
nn['equal_cum_wealth'] = eq_cum_wealth

nn['diff=bandit-equal'] = map(operator.sub,realized_return_list,eq_returns)
nn.to_csv('results{}.csv'.format(LAG), index=False)
#cw2 = get_cumulative_wealth()

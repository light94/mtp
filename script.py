from yahoo_finance import Share
import numpy as np
import pandas as pd

stock_list = ['YHOO','GOOGL']
historical_data = pd.DataFrame(columns=stock_list)
START_DATE = '2017-01-01'
END_DATE = '2017-03-16'

def get_data():
    global historical_data
    for stock in stock_list:
        share = Share(stock)
        data = share.get_historical(START_DATE, END_DATE)
        price_data = [daily_data['Close'] for daily_data in data]
        historical_data[stock] = pd.Series(price_data)
    historical_data = historical_data.astype(float)

def get_returns():
    historical_data_shift = historical_data.iloc[1:,:].copy().append(historical_data.tail(1))
    historical_data_shift.reset_index(inplace=True, drop=True)
    historical_data_shift = historical_data_shift.astype(float)
    returns = historical_data_shift / historical_data
    return returns

def get_covariance(returns_k):
    return  returns_k.cov()

def get_eigen(covariance):
    w, v = np.linalg.eig(covariance)
    return w,v

def get_normalized(mat):
    sums = mat.sum(axis=0)
    for i in range(mat.shape[1]):
        mat[:,i] = mat[:,i] / sums[i]

get_data()
returns = get_returns()

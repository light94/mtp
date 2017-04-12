import numpy as np
import pandas as pd
from operator import itemgetter, add
import os.path

stock_list = ['ADSEZ IB Equity','APNT IB Equity','AXSB IB Equity','BJAUT IB Equity','BHARTI IB Equity','CIPLA IB Equity','COAL IB Equity',
        'DRRD IB Equity','GAIL IB Equity','HDFC IB Equity','HDFCB IB Equity','HMCL IB  Equity','HUVR IB  Equity','ICICIBC IB  Equity','INFO IB  Equity',
        'ITC IB Equity','LT IB Equity','LPC IB  Equity','MM IB  Equity','MSIL IB  Equity','NTPC IB  Equity','ONGC IB  Equity','PWGR IB  Equity','RIL IB  Equity','SBIN IB  Equity',
        'SUNP IB  Equity','TTMT IB  Equity','TATA IB  Equity','TCS IB  Equity','WPRO IB  Equity']

START_DATE = '2012-01-01'
END_DATE = '2017-03-16'
num_rows = 0
num_stocks = len(stock_list)
arm_select_count = [0] * num_stocks
BACKUP = 250

def get_data():
    historical_data = pd.DataFrame(columns=stock_list)
    for stock in stock_list:
        print stock
        share = Share(stock)
        try:
            data = share.get_historical(START_DATE, END_DATE)
        except Exception as e:
            data = share.get_historical(START_DATE, END_DATE)
        price_data = [daily_data['Close'] for daily_data in data]
        historical_data[stock] = pd.Series(price_data)
    historical_data = historical_data.astype(float)
    return historical_data

def get_returns(historical_data):
    historical_data_shift = historical_data.iloc[1:,:].copy().append(historical_data.tail(1))
    historical_data_shift.reset_index(inplace=True, drop=True)
    historical_data_shift = historical_data_shift.astype(float)
    returns = (historical_data_shift / historical_data - 1)*100
    return returns

def get_covariance(returns, k):
    return  np.round(returns.iloc[k-BACKUP:k,:].cov(),4)

def get_eigen(covariance):
    w, v = np.linalg.eigh(covariance)
    return w,v

def get_normalized(mat):
    sums = mat.sum(axis=0)
    for i in range(mat.shape[1]):
        mat[:,i] = mat[:,i] / sums[i]

def get_normalized_vector(vect):
    return (vect/vect.sum())

def get_sharpe_ratio(returns, k):
    sr = [0] * num_stocks
    confidence_bound = [0] * num_stocks
    for i in range(num_stocks):
        sr[i] = np.dot(eigen_vectors[:,i], returns.iloc[k-BACKUP:k,:].mean(axis=0)) / np.sqrt(eigen_values[i])
        confidence_bound[i] = np.sqrt(2*np.log(k+num_rows)/(num_rows + arm_select_count[i]))
    return sr, confidence_bound

def adjust_matrices(eigens, returns_temp):
    global eigen_vectors, eigen_values
    col_list = []
    eigen_vectors_new = np.zeros(shape=(num_stocks,num_stocks))
    eigen_values_new = []
    i=0
    for index, cutoff in eigens:
        col_list.append(stock_list[index])
        eigen_vectors_new[:,i] = eigen_vectors[:,index]
        eigen_values_new.append(eigen_values[index])
        i+=1
    returns = returns_temp[col_list]
    eigen_vectors = eigen_vectors_new
    eigen_values = eigen_values_new
    return returns

def parition_arms(eigens):
    drops = []
    for i in range(len(eigens)-1):
        drops.append(eigens[i]/eigens[i+1])
    index, cutoff = max(enumerate(drops), key=itemgetter(1))
    # need to check for boundary conditions here
    return index

def get_optimal_arm(cutoff_index,ratios):
    global arm_select_count
    print 'arm_select_count {} '.format(arm_select_count)
    # significant
    index_sig, elem_sig = max(enumerate(ratios[:cutoff_index+1]), key=itemgetter(1))
    # insignificant
    index_insig, elem_insig = max(enumerate(ratios[cutoff_index+1:]), key=itemgetter(1))
    # index_sig and index_insig stll refer to the original index
    print 'index_sig = {}, index_insig= {}'.format(index_sig, index_insig)
    arm_select_count[index_sig] += 1
    arm_select_count[index_insig] += 1
    return index_sig, index_insig

def get_portfolio_variance(portfolio_index):
    return eigen_values[portfolio_index]/np.square(np.sum(eigen_vectors[:,portfolio_index]))

def get_portfolio_weights(index1, index2):
    var1 = get_portfolio_variance(index1)
    var2 = get_portfolio_variance(index2)
    theta =  var1/(var1+var2)
    h1 = eigen_vectors[:,index1]
    h2 = eigen_vectors[:,index2]

    return (1-theta)*h1 + theta*h2


def get_cumulative_wealth():
    cw = 1
    for i in range(len(realized_return_list)):
        cw *= (1+realized_return_list[i]/100)
    return cw

if os.path.isfile('historical_data_bl.csv'):
    historical_data = pd.read_csv('historical_data_bl.csv')
else:
    historical_data =  get_data()

returns = get_returns(historical_data)
num_rows = returns.shape[0]
realized_return_list = []

for k in range(BACKUP,num_rows):
    print 'k is {}'.format(k)
    eigen_values, eigen_vectors = get_eigen(get_covariance(returns,k))
    print 'Eigen values = {} \n'.format(eigen_values)
    sorted_eigens = sorted(enumerate(eigen_values), reverse=True, key=itemgetter(1))
    eigen_vectors_new = np.zeros(shape=(num_stocks,num_stocks))
    i = 0
    for index, value in sorted_eigens:
        eigen_vectors_new[:,i] = eigen_vectors[:,index]
        i+=1
    eigen_vectors = eigen_vectors_new
    cutoff_index = parition_arms(eigen_values)
    print 'cutoff index is {}'.format(cutoff_index)
    #returns_temp = adjust_matrices(sorted_eigens,returns_temp)
    sharpe_ratios, confidence_bound = get_sharpe_ratio(returns, k)
    index_sig, index_insig = get_optimal_arm(cutoff_index,map(add,sharpe_ratios,confidence_bound))
    weights = get_portfolio_weights(index_sig, index_insig)
    print 'Weights = {} \n'.format(weights)
    realized_return = np.dot(weights,returns.iloc[k,:])
    print 'Realized returns = {} \n'.format(realized_return)
    realized_return_list.append(realized_return)
cw = get_cumulative_wealth()
print cw

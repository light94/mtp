from yahoo_finance import Share
import pandas as pd

stock_list = ['YHOO','GOOGL']
historical_data = pd.DataFrame(columns=stock_list)
START_DATE = '2017-01-01'
END_DATE = '2017-03-16'
for stock in stock_list:
    share = Share(stock)
    data = share.get_historical(START_DATE, END_DATE)
    price_data = [daily_data['Close'] for daily_data in data]
    historical_data[stock] = pd.Series(price_data)

historical_data_shift = historical_data.iloc[1:,:].append(historical_data.tail(1))
historical_data_shift.reset_index(inplace=True, drop=True)
# convert to floats
historical_data = historical_data.astype(float)
historical_data_shift = historical_data_shift.astype(float)


returns = historical_data_shift / historical_data

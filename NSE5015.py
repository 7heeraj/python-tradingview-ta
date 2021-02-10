
# coding: utf-8

# In[ ]:
import pandas as pd
from tradingview_ta import TA_Handler, Interval
from tqdm import trange
import time
import datetime as dt
#########
tickers=pd.read_csv('dataset/ind_nifty50list.csv')
tickers=pd.DataFrame(tickers.Symbol)
########
dictionary = {'-':'_', '&':'_'}
tickers.replace(dictionary, regex=True, inplace=True)
Stock={}
handler = TA_Handler()
handler.set_exchange_as_crypto_or_stock("NSE")
handler.set_screener_as_stock("india")
tickers['Strength']=0
while True:
    handler.set_interval_as(Interval.INTERVAL_15_MINUTES)
    # tickers.shape[0]
    for i in trange(tickers.shape[0]):
        try:
            handler.set_symbol_as(tickers.Symbol[i])
            Stock[tickers.Symbol[i]]=[handler.get_analysis().summary['RECOMMENDATION'],handler.get_analysis().indicators['close']]
            #print([i],tickers[i],handler.get_analysis().summary['RECOMMENDATION'])
            
        except:
            print("An exception occurred",tickers[i])

    Stocks_df=pd.DataFrame.from_dict(Stock, orient='index',columns=['RECOMMENDATION','Price']).reset_index()
    # Stocks_df.head()
    STRONG_BUY=Stocks_df[Stocks_df.RECOMMENDATION=='STRONG_BUY'].reset_index(drop=True)
    # STRONG_BUY.head(10)   
    for i in range(STRONG_BUY.shape[0]):
        for j in range(tickers.shape[0]):
            if STRONG_BUY['index'][i] ==tickers['Symbol'][j]:
                #print(STRONG_BUY['index'][i])
                #Stocks_df=Stocks_df.copy()
                #print(Stocks_df.at[j,'Strength'])
                tickers.at[j,'Strength']+=1
                #print(Stocks_df.at[j,'Strength'])
        
    print(tickers)
    today = dt.datetime.today().strftime('%m%d%Y')  
    output_file = 'output\{}.csv'.format(today)
    tickers.to_csv(output_file, index = False)
    print('####################')
    print(STRONG_BUY)
    print('####################')
    BUY=Stocks_df[Stocks_df.RECOMMENDATION=='BUY'].reset_index(drop=True)
    print(BUY)
    print('####################')
    STRONG_SELL=Stocks_df[Stocks_df.RECOMMENDATION=='STRONG_SELL'].reset_index(drop=True)
    # STRONG_SELL.head(10)
    print(STRONG_SELL)
    print('####################')




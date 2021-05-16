# -*- coding: utf-8 -*-
"""
Created on Fri May 14 09:11:00 2021

@author: w

"""


import mplfinance as mpf
import pandas as pd
import date0513p2

kbar = date0513p2.data_dict

kbar_df = pd.DataFrame(kbar)
kbar_df.columns = [ i.capitalize() for i in kbar_df.columns ]
kbar_df.set_index("Time", inplace=True)


#mpf.plot(kbar_df[-100:])
#mpf.plot(kbar_df[-100:], type='candle')
#mpf.plot(kbar_df[-100:], type='candle', style='charles')
#mpf.plot(kbar_df, volume=True,type='candle', style='charles')

# def getStockdaily_df(stockno):
#     kbar=getStockdaily_dict(stockno)
#     kbar_df = pd.DataFrame(kbar)
#     kbar_df.columns = [ i.capitalize() for i in kbar_df.columns]
#     kbar_df.set_index("Time", inplace=True)
#     return kbar_df


#def chartKbar(stockno):
    #getStockdaily_df
    
    
#def chartKbar_dict(kbar):
    # kbar_df = pd.DataFrame(kbar)
    # kbar_df.columns = [ i.capitalize() for i in kbar_df.columns]
    # kbar_df.set_index("Time", inplace=True)
    kab
index=0
for i in range(20, len(kbar['time'])-1):
    c_time = kbar['time'][i]

    c_close = kbar['close'][i]
    
    last_20_high = max(kbar['high'][i-20:i])
    last_20_low = min(kbar['low'][i-20:i])
    
    next_open = kbar['open'][i+1]
    next_time = kbar['time'][i+1]

    
    if index == 0 and c_close > last_20_high:
        #BUY
        index = 1
        order_time = next_time
        order_price = next_open
        #加or減
        stop_loss = round( (last_20_high + last_20_low) / 2 )
        take_profit = round((last_20_high - last_20_low) + order_price)
        print("進場時間:%s 進場價格:%s 停利價位:%s 停損價位:%s "%(
            order_time, order_price, take_profit, stop_loss,), end=' ')
        continue
    elif index == 1:

            if c_close >= take_profit:
                index = 0
                cover_time = next_time
                cover_price = next_open
                
                print("停利 出場時間:%s 出場價格:%s " %(cover_time, cover_price))
                continue
            elif c_close <= stop_loss:
                index = 0
                cover_time = next_time
                cover_price = next_open
        
                print("停損 出場時間:%s 出場價格:%s " %(cover_time, cover_price))
                continue
    
    
    
    # print(current_time)
    # print(kbar['open'][i])
    # print(kbar['high'][i])
    # print(kbar['low'][i])
    # print(kbar['close'][i])
    

    
    
    
    
    
    
    
    
    
    
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 13:33:43 2021

@author: w
"""

from datetime import datetime
f=open('0050.csv','r',encoding="utf-8")

data = [i.strip('\n').strip('\ufeff').split(',') for i in f.readlines() ]
stockNo='0050'
total_data = []    

for row in data:
    row[0]=datetime.strptime(row[0],"%m/%d/%Y").strftime("%Y-%m-%d")

    row.insert(0, "0050")
    #print(row)
import pandas
import numpy

df = pandas.DataFrame(data)
#print(df)

data_dict={}

data_dict['symbol']=df[0].to_numpy()
data_dict['time']=df[1].to_numpy(dtype="datetime64")

data_dict['open']=df[4].to_numpy(dtype="float")
data_dict['high']=df[5].to_numpy(dtype="float")
data_dict['low']=df[6].to_numpy(dtype="float")
data_dict['close']=df[7].to_numpy(dtype="float")

data_dict['volume']=df[6].to_numpy(dtype="float")

data_dict['match_count']=df[2].to_numpy(dtype="float")
data_dict['match_value']=df[3].to_numpy(dtype="float")


kbar = data_dict

# kbar_df = pd.DataFrame(kbar)
# kbar_df.columns = [ i.capitalize() for i in kbar_df.columns ]
# kbar_df.set_index("Time", inplace=True)

trade_record=[]

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

            #if c_close < order_price + stop_loss:
            if c_close >= take_profit:
                index = 0
                cover_time = next_time
                cover_price = next_open
                
                print("停利 出場時間:%s 出場價格:%s " %(cover_time, cover_price))
                trade_record.append(['B', order_time, order_price, cover_time, cover_price ])
                continue
            elif c_close <= stop_loss:
                index = 0
                cover_time = next_time
                cover_price = next_open
        
                print("停損 出場時間:%s 出場價格:%s " %(cover_time, cover_price))
                trade_record.append(['B', order_time, order_price, cover_time, cover_price ])
                continue
            

print(trade_record)

total_profit = [ i[4]-i[2] for i in trade_record if i[0] =='B']

print(total_profit)
print('總績效', sum(total_profit))
print('平均績效', sum(total_profit)/len(total_profit))
earn_total_profit = [i for i in total_profit if i > 0]
loss_total_profit = [i for i in total_profit if i <= 0]


print('勝率', len(earn_total_profit)*100 / len(total_profit),"%")
print('平均獲利', sum(earn_total_profit)/len(total_profit))
print('平均損失', sum(loss_total_profit)/len(total_profit))

max_loss=0
current_max_loss=0
for i in total_profit:
    if i < 0:
        current_max_loss += i
        if current_max_loss < max_loss:
            max_loss = current_max_loss
    elif i > 0:
        current_max_loss = 0
                  
print('最大連續虧損', max_loss)
print('獲利因子',sum(earn_total_profit) /abs(sum(loss_total_profit)))

import mplfinance as mpf
#chartKbar_dict


#K  & k case
Kbar_df = pandas.DataFrame(kbar)
Kbar_df.columns = [ i.capitalize() for i in Kbar_df.columns ]
Kbar_df.set_index("Time", inplace=True)
print(Kbar_df)

BTR = [ i for i in trade_record if i[0] =='B' ]
BuyOrderPoint = []
BuyCoverPoint = []
for date, value in Kbar_df['Close'].iteritems():
    if date in [ i[1] for i in BTR]:
        BuyOrderPoint.append( Kbar_df['Low'][date] * 0.999)
    else:
        BuyOrderPoint.append(numpy.nan)
    if date in [ i[3] for i in BTR]:
        BuyCoverPoint.append( Kbar_df['High'][date] * 1.001)
    else:
        BuyCoverPoint.append(numpy.nan)


addp = []

addp.append(
    mpf.make_addplot(BuyOrderPoint, scatter= True, markersize=100, marker='^',color='red' )
    )
addp.append(
    mpf.make_addplot(BuyOrderPoint, scatter= True, markersize=100, marker='v',color='blue' )
    )

mpf.plot(Kbar_df,addplot=addp, volume=False,type='candle', style='charles')


#justtestfor git
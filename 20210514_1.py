from myfunc import getStockDaily_dict,chartKbar_dict
# 取得資料 dictionary 格式 # 計算技術指標
kbar = getStockDaily_dict( '0050' )

# 交易紀錄的物件
trade_record=[]
# 儲存目前部位的變數
index=0
# 回測的方式 
for i in range(20,len(kbar['time'])-1):
    c_time=kbar['time'][i]
    c_close=kbar['close'][i]
    last_20_high=max(kbar['high'][i-20:i])
    last_20_low=min(kbar['low'][i-20:i])
    n_open=kbar['open'][i+1]
    n_time=kbar['time'][i+1]
    
    # 當目前部位空手 收盤價 大於前20日的最高價 買進
    if index == 0 and c_close > last_20_high:
        # 買進
        index = 1
        order_time = n_time
        order_price = n_open
        stop_loss = round((last_20_high + last_20_low )/2)
        take_profit = round(order_price + (last_20_high - last_20_low ))
        print('進場時間:%s 進場價格:%s 停利價位:%s 停損價位:%s' % (order_time,order_price,take_profit,stop_loss) ,end=' ' )
        continue
    # 如果目前部位是多方 
    elif index == 1:
        # 收盤價 大於 停利點
        if c_close >= take_profit:
            index = 0 
            cover_time = n_time
            cover_price = n_open
            print('停利 出場時間:%s 出場價格:%s' % (cover_time,cover_price))
            # 加入交易紀錄
            trade_record.append(['B',order_time,order_price,cover_time,cover_price])
            continue
        # 收盤價 小於 停損點 
        elif c_close <= stop_loss:
            index = 0 
            cover_time = n_time
            cover_price = n_open
            print('停損 出場時間:%s 出場價格:%s' % (cover_time,cover_price))
            # 加入交易紀錄
            trade_record.append(['B',order_time,order_price,cover_time,cover_price])
            continue
        
# 計算績效指標 -------------------------------------
total_profit=[ i[4]-i[2] for i in trade_record if i[0]=='B' ]
# 總績效 總次數
print('\n總績效',sum(total_profit),'總次數',len(total_profit))
# 平均績效
print('平均績效',sum(total_profit)/len(total_profit))
# 平均獲利 平均損失 勝率
earn_total_profit=[ i for i in total_profit if i > 0 ]
loss_total_profit=[ i for i in total_profit if i <= 0 ]
print('平均獲利',sum(earn_total_profit)/len(earn_total_profit))
print('平均損失',sum(loss_total_profit)/len(loss_total_profit))
print('勝率',len(earn_total_profit) / len(total_profit))
# 最大連續虧損
max_loss=0
current_max_loss=0
for i in total_profit:
    if i <= 0:
        current_max_loss += i
        if current_max_loss < max_loss:
            max_loss = current_max_loss
    else:
        current_max_loss = 0 
print('最大連續虧損',max_loss)
# 獲利因子 # 賠一元 可以賺多少 
print('獲利因子',sum(earn_total_profit)/abs(sum(loss_total_profit)))
    
# 計算績效指標 -------------------------------------
    
# 計算繪製策略圖 -------------------------------------

import pandas as pd 
import numpy 
import mplfinance as mpf
Kbar_df=pd.DataFrame(kbar)
Kbar_df.columns = [ i[0].upper()+i[1:] for i in Kbar_df.columns ]
Kbar_df.set_index( "Time" , inplace=True)
BTR = [ i for i in trade_record if i[0]=='B' ]
BuyOrderPoint = [] 
BuyCoverPoint = []

for date,value in Kbar_df['Close'].iteritems():
    # 日期 在 買方 進場 交易記錄內 
    if date in [ i[1] for i in BTR ]:
        # 新增一個值 最低點的 下面
        BuyOrderPoint.append( Kbar_df['Low'][date] * 0.999 )
    else:
        # nan
        BuyOrderPoint.append(numpy.nan)
    if date in [ i[3] for i in BTR ]:
        # 
        BuyCoverPoint.append( Kbar_df['High'][date] * 1.001 )
    else:
        # 
        BuyCoverPoint.append(numpy.nan)
# add plot      
addp=[]
addp.append(mpf.make_addplot(BuyOrderPoint,scatter=True,markersize=200,marker='^',color='red'))
addp.append(mpf.make_addplot(BuyCoverPoint,scatter=True,markersize=200,marker='v',color='blue'))
mpf.plot(Kbar_df,addplot=addp,volume=True,type='candle',style='charles')





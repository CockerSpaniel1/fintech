from myfunc import *
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
    
    if index == 0 :
        if c_close > last_20_high:
            # 買進
            index = 1
            order_time = n_time
            order_price = n_open
            # 停損點
            stop_loss = round((last_20_high + last_20_low )/2)
            # 停損的點數
            stop_loss_number = order_price - stop_loss
            print('多方進場時間:%s 進場價格:%s 停損價位:%s' % (order_time,order_price,stop_loss) ,end=' ' )
            continue
        # 當價格 向下突破
        if c_close < last_20_low:
            index = -1
            order_time = n_time
            order_price = n_open
            # 停損點
            stop_loss = round((last_20_high + last_20_low )/2)
            # 停損的點數
            stop_loss_number = stop_loss-order_price 
            print('空方進場時間:%s 進場價格:%s 停損價位:%s' % (order_time,order_price,stop_loss) ,end=' ' )
            continue
    # 如果目前部位是多方 
    elif index == 1:
        # 如果收盤價減去停損點數 大於 停損價位 則 上修停損價位 
        if c_close - stop_loss_number >= stop_loss:
            stop_loss = c_close - stop_loss_number
        # 收盤價 小於 停損點  ( 當漲幅 大於 停損的點數 這時候觸發到停損時 會是獲利的 )
        elif c_close <= stop_loss:
            index = 0 
            cover_time = n_time
            cover_price = n_open
            print('停損 出場時間:%s 出場價格:%s' % (cover_time,cover_price))
            # 加入交易紀錄
            trade_record.append(['B',order_time,order_price,cover_time,cover_price])
            continue
    # 如果目前部位是空方 
    elif index == -1:
        # 如果收盤價加上停損點數 小於 停損價位 則 下修停損價位 
        if c_close + stop_loss_number <= stop_loss:
            stop_loss = c_close + stop_loss_number
        # 收盤價 大於 停損點  ( 當跌幅 大於 停損的點數 這時候觸發到停損時 會是獲利的 )
        elif c_close >= stop_loss:
            index = 0 
            cover_time = n_time
            cover_price = n_open
            print('停損 出場時間:%s 出場價格:%s' % (cover_time,cover_price))
            # 加入交易紀錄
            trade_record.append(['S',order_time,order_price,cover_time,cover_price])
            continue
        
# 計算績效指標 
getPerformance(trade_record)
    
# 計算繪製策略圖 
# chartOrder(kbar,trade_record)





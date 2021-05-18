import pymysql,numpy,datetime
import pandas as pd 
import numpy 
import mplfinance as mpf

"""
def getStockDaily_sql( stockno ):
    # localhost = 127.0.0.1
    conn=pymysql.connect(host='localhost', port=3306, user="root",passwd="123456",db="fintech")
    # 建立工作環境(游標)
    cur = conn.cursor()
    # 執行select sql query
    cur.execute('select * from stock_daily where symbol="%s"' % (stockno) )
    # 將select 結果取出
    tmplist =[]
    for row in cur:
        tmplist.append(row)
    return tmplist
    
def getStockDaily_dict( stockno ):
    data=getStockDaily( stockno )
    data_dict ={}
    # ('2014', datetime.date(2021, 5, 12), 57.3, 59.3, 51.0, 51.0, 210542735, 81294, 11569159228)
    data_dict['time'] = numpy.array([ i[1] for i in data ])
    data_dict['symbol'] = numpy.array([ i[0] for i in data ])
    data_dict['open'] = numpy.array([ i[2] for i in data ])
    data_dict['high'] = numpy.array([ i[3] for i in data ])
    data_dict['low'] = numpy.array([ i[4] for i in data ])
    data_dict['close'] = numpy.array([ i[5] for i in data ])
    data_dict['volume'] = numpy.array([ float(i[6]) for i in data ])
    data_dict['match_count'] = numpy.array([ float(i[7]) for i in data ])
    data_dict['match_value'] = numpy.array([ float(i[8]) for i in data ])
    return data_dict
   
"""

# 20210514 _______________

import pandas as pd 
import mplfinance as mpf

def getStockDaily( stockno ):
    #path='C:\\Users\\jack\\Desktop\\pythonsample\\'
    f=open(stockno+'.csv')
    data = [ i.strip('\n').split(',') for i in f ]
    data = [ [stockno,datetime.datetime.strptime(i[0],'%Y/%m/%d'),float(i[3]),float(i[4]),float(i[5]),float(i[6]),float(i[1]),float(i[8]),float(i[2])]  for i in data ] 
    return data
    
def getStockDaily_dict( stockno ):
    data=getStockDaily( stockno )
    data_dict ={}
    data_dict['time'] = numpy.array([ i[1] for i in data ])
    data_dict['symbol'] = numpy.array([ i[0] for i in data ])
    data_dict['open'] = numpy.array([ i[2] for i in data ])
    data_dict['high'] = numpy.array([ i[3] for i in data ])
    data_dict['low'] = numpy.array([ i[4] for i in data ])
    data_dict['close'] = numpy.array([ i[5] for i in data ])
    data_dict['volume'] = numpy.array([ float(i[6]) for i in data ])
    data_dict['match_count'] = numpy.array([ float(i[7]) for i in data ])
    data_dict['match_value'] = numpy.array([ float(i[8]) for i in data ])
    return data_dict
    
def getStockDaily_df(stockno):
    kbar=getStockDaily_dict( stockno )
    Kbar_df=pd.DataFrame(kbar)
    Kbar_df.columns = [ i[0].upper()+i[1:] for i in Kbar_df.columns ]
    Kbar_df.set_index( "Time" , inplace=True)
    return Kbar_df
    
def chartKbar(stockno):
    Kbar_df=getStockDaily_df(stockno)
    mpf.plot(Kbar_df,volume=True,type='candle',style='charles')
    
def chartKbar_dict(Kbar):
    Kbar_df=pd.DataFrame(Kbar)
    Kbar_df.columns = [ i[0].upper()+i[1:] for i in Kbar_df.columns ]
    Kbar_df.set_index( "Time" , inplace=True)
    mpf.plot(Kbar_df,volume=True,type='candle',style='charles')
    
def chartOrder(Kbar,TR):
    Kbar_df=pd.DataFrame(Kbar)
    Kbar_df.columns = [ i[0].upper()+i[1:] for i in Kbar_df.columns ]
    Kbar_df.set_index( "Time" , inplace=True)
    
    # add plot      
    addp=[]
    BTR = [ i for i in TR if i[0]=='B' ]
    # 如果我有買方 交易紀錄的話 圖表才顯示買方交易
    if BTR != []:
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
                BuyCoverPoint.append( Kbar_df['High'][date] * 1.001 )
            else:
                BuyCoverPoint.append(numpy.nan)
        addp.append(mpf.make_addplot(BuyOrderPoint,scatter=True,markersize=200,marker='^',color='red'))
        addp.append(mpf.make_addplot(BuyCoverPoint,scatter=True,markersize=200,marker='v',color='blue'))
    STR = [ i for i in TR if i[0]=='S' ]
    if STR != []:
        SellOrderPoint = [] 
        SellCoverPoint = []
        for date,value in Kbar_df['Close'].iteritems():
            # 日期 在 賣方 進場 交易記錄內 
            if date in [ i[1] for i in STR ]:
                # 新增一個值 最高點的 上面
                SellOrderPoint.append( Kbar_df['High'][date] * 1.001 )
            else:
                # nan
                SellOrderPoint.append(numpy.nan)
            if date in [ i[3] for i in STR ]:
                SellCoverPoint.append( Kbar_df['Low'][date] * 0.999 )
            else:
                SellCoverPoint.append(numpy.nan)
        addp.append(mpf.make_addplot(SellOrderPoint,scatter=True,markersize=200,marker='v',color='green'))
        addp.append(mpf.make_addplot(SellCoverPoint,scatter=True,markersize=200,marker='^',color='blue'))
    
    mpf.plot(Kbar_df,addplot=addp,volume=True,type='candle',style='charles')
    
def getPerformance(TR):
    # total_profit=[ i[4]-i[2] for i in TR if i[0]=='B' ]
    total_profit = []
    for i in TR:
        if i[0] == 'B':
            total_profit.append(i[4]-i[2])
        elif i[0] == 'S':
            total_profit.append(i[2]-i[4])
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

# -*- coding: utf-8 -*-
"""
Created on Thu May 13 13:49:53 2021

@author: w.strip('\ufeff')
"""
#import pymysql
from datetime import datetime
f=open('2014q.csv','r',encoding="utf-8")

data = [i.strip('\n').strip('\ufeff').split(',') for i in f.readlines() ]
stockNo='2014'
total_data = []    
#print(datetime.strptime(data[0][0],"%d/%m/%Y").strftime("%Y-%m-%d"))

#localhost =127.0,0,1
#conn = pymysql.connect(host='localhost', port=3308, user="root",passwd="076429575",db="fintech")
#建立工作游標
#cur = conn.cursor()
#執行sql query
# =============================================================================
for row in data:
    row[0]=datetime.strptime(row[0],"%m/%d/%Y").strftime("%Y-%m-%d")
    #execstr="insert into stock_daily() value ('%s','%s','%s','%s','%s','%s','%s','%s','%s');" % ('2014', row[0], row[3], row[4], row[5], row[6], row[1], row[8], row[2])
    #cur.execute(execstr)
    #print(execstr)
    row.insert(0, "2014")
    #print(row)
# =============================================================================


# cur.execute("Select * From stock_daily")
# #將select 結果取出
# for row in cur:
#     print(row)

#cur.execute("insert into stock_daily() value('2015', '2021/1/4','16.5','16.85','15.9','16.5','96986569','24502','1586464254');")

#getStockDailysql
# def getStockDaily(stockno);:
    
    
#     conn=
#     cur=
#     cur.execute

#     tmplits=[]
#     for row in cur" 
#         tmplist.apppend(row)
#     return templist

#conn.commit()
# cur.close()
# conn.close()

#def getStockdaily_dict(stockno):
    #getStockdaily(stockno)
    # path = ""
    # f= open(path+stockNo+'.csv')
    # data  = [i]
    # return data


import pandas 
import numpy
#data
df = pandas.DataFrame(data)
#print(df)

data_dict={}
# data_dict['time']=df[1].to_list()
# data_dict['symbol']=df[0].to_list()
# data_dict['open']=df[2].to_list()
# data_dict['high']=df[3].to_list()
# data_dict['low']=df[4].to_list()
# data_dict['close']=df[5].to_list()
# data_dict['vollume']=df[6].to_list()
# data_dict['match_count']=df[7].to_list()
# data_dict['match_value']=df[8].to_list()

data_dict['symbol']=df[0].to_numpy()
data_dict['time']=df[1].to_numpy(dtype="datetime64")

data_dict['open']=df[4].to_numpy(dtype="float")
data_dict['high']=df[5].to_numpy(dtype="float")
data_dict['low']=df[6].to_numpy(dtype="float")
data_dict['close']=df[7].to_numpy(dtype="float")

data_dict['volume']=df[6].to_numpy(dtype="float")

data_dict['match_count']=df[2].to_numpy(dtype="float")
data_dict['match_value']=df[3].to_numpy(dtype="float")


print(data_dict)


#kbar=getStockDaily_dict('2014')


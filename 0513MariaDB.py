# -*- coding: utf-8 -*-
"""
Created on Thu May 13 10:35:49 2021

@author: w
"""

import pymysql
import datetime
import time
import requests
import json

# =============================================================================
# #import C0512
# 
# #localhost =127.0,0,1
# conn = pymysql.connect(host='localhost', port=3308, user="root",passwd="076429575",db="fintech")
# #建立工作游標
# cur = conn.cursor()
# #執行sql query
# cur.execute("Select * From stock_daily")
# #將select 結果取出
# for row in cur:
#     print(row)
# 
# cur.execute("insert into stock_daily() value('2015', '2021/1/4','16.5','16.85','15.9','16.5','96986569','24502','1586464254');")
# 
# conn.commit()
# 
# 
# =============================================================================

begin = datetime.datetime.strptime('2005/01/01', '%Y/%m/%d')

end = datetime.datetime.strptime('2021/05/01', '%Y/%m/%d')

date_list = []
while begin <= end:
    date_str=begin.strftime('%Y/%m/%d')
    date_list.append(date_str)
    begin += datetime.timedelta(days=31)
    begin = begin.replace(day=1)

# print(date_list)
#x = C0512.crawlbymonth(['99/04/01'])


response='json'
stockNo='2014'
timestamp='1620788644990'



def ConverYear(stringdate):
    l = stringdate.split('/')
    l[0] = str( int(l[0]) + 1911)
    return "/".join(l)

# for date in date_lisfor i in range(1):    

date='20160401'
url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response={response}&date={date}&stockNo={stockNo}&_={timestamp}'

res = requests.get(url)
dict_data = json.loads(res.text)


total_data = [] 
  
for row in dict_data["data"]:  
    row[0] = ConverYear(row[0])
    row=[i.replace(",", "") for i in row]
    print(row) 
            
    total_data.append(row)
    print(date, '爬蟲成功')    
    #     #time.sleep(5)
    except:
    #     print(date, '爬蟲失敗')
    #     break
    
     

# =============================================================================
for row in total_data:
    execstr="insert into stock_daily() value('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',);"
    %(stockNo, row[0], row[3], row[4], row[5], row[6], row[0], row[1], row[8], row[2])
# =============================================================================
    
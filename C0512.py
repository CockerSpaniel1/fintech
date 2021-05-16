# -*- coding: utf-8 -*-
"""
Created on Wed May 12 09:20:14 2021

@author: w
"""

import requests, json

from bs4 import BeautifulSoup


# =============================================================================
# html=requests.get("https://tw.stock.yahoo.com/rank/turnover")
# htmltext=html.text
# 
# soup = BeautifulSoup(htmltext, "lxml")
# 
# ul = soup.find('ul', class_= "M(0) P(0) List(n)")
# 
# 
# #class_='Pos(a) W(100%) H(100%) T(0) Start(0) Z(0)')
# #Path = "C:\\Users\\w\\filenma.csv"
# with open('test0512.csv', 'w') as f:
#     for li in ul.find_all('li'):
#         templist=[]
#         #print(li)
#         obj = li.find('a')
#         #print(a)
#         for _ in range(11):
#             obj = obj.findNext('div')
#             
#             #print(obj.text)
#     
#             objtext = obj.text.replace("," , "")
#             #空值資料 不加入list  
#             if objtext != "":
#                 templist.append(objtext)
#         #print(templist)
#         #print(",".join(templist))
#         f.write(",".join(templist) + "\n")
#     
# =============================================================================
import time

def ConverYear(stringdate):
    l = stringdate.split('/')
    l[0] = str( int(l[0]) + 1911)
    return "/".join(l)


response='json'
stockNo='2330'
timestamp='1620788644990'
    

total_data = []

def crawlbymonth(date_list):
    for date in date_list:
        try:
            #date='20210401'
            url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response={response}&date={date}&stockNo={stockNo}#&_={timestamp}'
            
            res = requests.get(url)
            data = json.loads(res.text)
            print(data)
        
            for row in data["data"]:
                # i[0] = str( int(i[0].split('/')[0]) + 1911 ) 
                row[0] = ConverYear(row[0])
                row=[i.replace(",", "") for i in row]
                #print(row) 
                
                total_data.append(row)
            print(date, '爬蟲成功')    
            time.sleep(5)
        except:
            print(date, '爬蟲失敗')
            break


x = crawlbymonth(['105/04/03'])
print(x)
# with open('test0513_1.csv', 'w') as f:
#     for row in total_data:
#         f.write(",".join(row) + "\n")
        
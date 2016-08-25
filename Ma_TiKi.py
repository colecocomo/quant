# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:12:28 2016

@author: colec
"""
import tushare as ts
import pandas as pd
import time
import csv

file_result = open("ma_TiKiResult.txt", "a+")
resultTime = time.localtime(time.time())
formatResultTime = time.strftime("%Y-%m-%d %H:%M:%S", resultTime)
file_result.write("--------------------------------------\n")
file_result.write(formatResultTime)
file_result.write("\n")
file_result.write("ma tiki-taka统计结果")
file_result.write("\n")
file_result.write("stock        ")
file_result.write("maDiffPercent5        ")
file_result.write("maDiffPercent10        ")
file_result.write("maDiffPercent20        ")
file_result.write("\n")

file_csv = open('ma_TiKi.csv', 'wb+')
spamwriter = csv.writer(file_csv,dialect='excel')
spamwriter.writerow(['stock', 'maDiffPercent5', 'maDiffPercent10', 'maDiffPercent20', "dayCnt"])

all_stock = ts.get_stock_basics()

curTime = time.localtime(time.time())
formatCurTime = time.strftime("%Y-%m-%d", curTime)
endTime = time.localtime(time.time() - 30 * 86400)
formatEndTime = time.strftime("%Y-%m-%d", endTime)

dates = pd.bdate_range(end= formatCurTime, periods = 30, freq="B")
print(dates)
datesList = dates.tolist()
print(datesList[0].to_datetime())

for code, stockRow in all_stock.iterrows():
    print("开始统计"+code)
    stockInfo = ts.get_h_data(code, \
                                start = str(datesList[0].to_datetime()), \
                                end = str(datesList[29].to_datetime()))
    if (stockInfo is None or stockInfo.empty):
        print(code + "停牌")
        file_result.write(code + "停牌")
        file_result.write("\n")
        continue
    dayCnt = 0
    idx = 0
    sumPrice = 0
    curPrice = 0
    ma5 = 0
    ma10 = 0
    ma20 = 0
    while(idx < 30):
        curStockInfo = stockInfo.get_value(datesList[idx])
        if(curStockInfo is None or curStockInfo.emppty()):
            print(code + "在日期" + datesList[idx] + "停牌")
            file_result.write(code + "在日期" + dates[idx] + "停牌")
            file_result.write("\n")
            idx += 1
            continue
        curPrice = int(curStockInfo["close"] * 100) 
        if(curPrice == 0):
            print(code + "在日期" + datesList[idx] + "停牌")
            file_result.write(code + "在日期" + datesList[idx] + "停牌")
            file_result.write("\n")
            idx += 1
            continue
        sumPrice += curPrice
        dayCnt += 1
        idx += 1
        if(dayCnt == 5):
            ma5 = int(sumPrice / 5)
        if(dayCnt == 10):
            ma10 = int(sumPrice / 10)
        if(dayCnt == 20):
            ma20 = int(sumPrice / 20)
    
    if(dayCnt < 5):
        print(code + "开市时间不足5天")
        file_result.write(code + "开市时间不足5天")
        file_result.write("\n")
        continue
    if(dayCnt < 10):
        ma10 = ma5
        ma20 = ma5
        continue
    if(dayCnt < 20):
        ma20 = ma10
        continue
            
    curPrice = float(stockInfo.at[datesList[29]]["close"])

    if(ma5 == 0):
        ma5 = curPrice
    else:
        ma5 = float(ma5 / 100)
    if(ma10 == 0):
        ma10 = curPrice
    else:
        ma10 = float(ma10 / 100)
    if(ma20 == 0):
        ma20 = curPrice
    else:
        ma20 = float(ma20 / 100)
    
    maDiffPercent5 = (ma5 - curPrice) / curPrice * 100
    maDiffPercent10 = (ma10 - curPrice) / curPrice * 100
    maDiffPercent20 = (ma20 - curPrice) / curPrice * 100
    
    print("ma5 " + str(maDiffPercent5) + \
          "    ma10" + str(maDiffPercent10) + \
          "    ma20" + str(maDiffPercent20))
          
          
    spamwriter.writerow([code, maDiffPercent5, maDiffPercent10, maDiffPercent20], dayCnt)
    
    file_result.write(code + "    ")
    file_result.write(str(maDiffPercent5) + "    ")
    file_result.write(str(maDiffPercent10) + "    ")
    file_result.write(str(maDiffPercent20) + "    ")
    file_result.write("\n")
file_csv.close()
file_result.close()
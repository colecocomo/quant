# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:12:28 2016

@author: colec
"""
import tushare as ts
import time
import csv

file_stock_id = open("AllStockID.txt", "r")
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
spamwriter.writerow(['stock', 'maDiffPercent5', 'maDiffPercent10', 'maDiffPercent20'])

all_stock = file_stock_id.readlines()
curTime = time.localtime(time.time())
formatCurTime = time.strftime("%Y-%m-%d", curTime)

for stock in all_stock:
    stockID = stock[0:6]
    stockInfo = ts.get_hist_data(stockID, \
                                start = formatCurTime, \
                                end = formatCurTime)
    if (stockInfo is None or stockInfo.empty):
        print(stockID + "停牌")
        file_result.write(stockID + "停牌")
        file_result.write("\n")
        continue
    ma5 = float(stockInfo["ma5"])
    ma10 = float(stockInfo["ma10"])
    ma20 = float(stockInfo["ma20"])
    curPrice = float(stockInfo["close"])
    
    maDiffPercent5 = (ma5 - curPrice) / curPrice * 100
    maDiffPercent10 = (ma10 - curPrice) / curPrice * 100
    maDiffPercent20 = (ma20 - curPrice) / curPrice * 100
    
    print("ma5 " + str(maDiffPercent5) + \
          "    ma10" + str(maDiffPercent10) + \
          "    ma20" + str(maDiffPercent20))
          
          
    spamwriter.writerow([stockID, maDiffPercent5, maDiffPercent10, maDiffPercent20])
    
    file_result.write(stockID + "    ")
    file_result.write(str(maDiffPercent5) + "    ")
    file_result.write(str(maDiffPercent10) + "    ")
    file_result.write(str(maDiffPercent20) + "    ")
    file_result.write("\n")
file_csv.close()
file_result.close()
file_stock_id.close()
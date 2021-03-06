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
spamwriter.writerow(['stock', 'maDiffPercent5', 'maDiffPercent10', 'maDiffPercent20', "dayCnt", "curStatus", "maxVolumePercentRecently"])

all_stock = ts.get_stock_basics()

curTime = time.localtime(time.time())
formatCurTime = time.strftime("%Y-%m-%d", curTime)
endTime = time.localtime(time.time() - 86400)
formatEndTime = time.strftime("%Y-%m-%d", endTime)

dates = pd.bdate_range(end= formatEndTime, periods = 30, freq="B")
datesList = dates.tolist()
actualEndTime = datesList[29].to_datetime()
actualEndTime = str(actualEndTime)[0:10]

for code, stockRow in all_stock.iterrows():
    print("statistic "+code)
    #print(stockRow)
    try:
        stockInfo = ts.get_h_data(code, \
                                start = str(datesList[0].to_datetime()), \
                                end = str(datesList[29].to_datetime()))
    except Exception, e:
        print(e.message.decode('utf-8').encode('gb2312'))
        try:
            stockInfo = ts.get_h_data(code, \
                                start = str(datesList[0].to_datetime()), \
                                end = str(datesList[29].to_datetime()))
        except Exception, e1:
            print("retry error" + e.message.decode('utf-8').encode('gb2312'))
            file_result.write(code + "获取数据错误")
            continue
    if (stockInfo is None or stockInfo.empty):
        print(code + " suspendion")
        file_result.write(code + " suspendion")
        file_result.write("\n")
        continue
    dayCnt = 0
    idx = 0
    sumPrice = 0
    curPrice = 0
    ma5 = 0.0
    ma10 = 0.0
    ma20 = 0.0
    lastDate = ''
    lastPrice = 0
    isGetLastDate = False
    volumeDayCnt = 0
    maxVolumePercent = 0
    volumePercnt = 0
    stockInfo = stockInfo.sort_index(ascending=False)
    for date, stockInfoRow in stockInfo.iterrows():
        #print('时间')
        #print(date)
        #print(stockInfoRow)
        if(volumeDayCnt < 5):
            volumePercent = (float(stockInfoRow["volume"] * 100) / float(stockRow["outstanding"] * 10000)) * 100
            maxVolumePercent = max(maxVolumePercent, volumePercent)
            volumeDayCnt += 1
        if(stockInfoRow is None):
            print(code + "at " + date + " suspendion")
            file_result.write(code + "at " + date + " suspendion")
            file_result.write("\n")
            idx += 1
            continue
        curPrice = int(stockInfoRow["close"] * 100) 
        if(curPrice == 0):
            print(code + "at " + date + " suspendion")
            file_result.write(code + "at " + date + " suspendion")
            file_result.write("\n")
            idx += 1
            continue

        if not isGetLastDate:
            lastDate = str(date)[0:10]
            lastPrice = curPrice
            isGetLastDate = True
        
        sumPrice += curPrice
        dayCnt += 1
        idx += 1
        if(dayCnt == 5):
            ma5 = int(sumPrice / 5)
        if(dayCnt == 10):
            ma10 = int(sumPrice / 10)
        if(dayCnt == 20):
            ma20 = int(sumPrice / 20)
    #print("dayCnt:" + str(dayCnt) + "cruPrice:" + str(lastPrice) + "sumPrice" + str(sumPrice))
    if(dayCnt < 5):
        print(code + "not enough trading data(at least 5 days)")
        file_result.write(code + "开市时间不足5天")
        file_result.write("\n")
        continue
    if(dayCnt < 10):
        ma10 = ma5
        ma20 = ma5
    if(dayCnt < 20):
        ma20 = ma10
        
    #print("ma5 " + str(ma5) + \
    #      "    ma10 " + str(ma10) + \
    #      "    ma20 " + str(ma20))
    
    maDiffPercent5 = float(ma5 - lastPrice) / float(lastPrice) * 100
    maDiffPercent10 = float(ma10 - lastPrice) / float(lastPrice) * 100
    maDiffPercent20 = float(ma20 - lastPrice) / float(lastPrice) * 100
    
    #print("ma5 " + str(maDiffPercent5) + \
    #      "    ma10" + str(maDiffPercent10) + \
    #      "    ma20" + str(maDiffPercent20))
         
    curStatus = "normal"
    #print(lastDate)
    #print(formatCurTime)
    #print(actualEndTime)
    if(lastDate != actualEndTime):
        curStatus = "suspendion"
          
    spamwriter.writerow([code, maDiffPercent5, maDiffPercent10, maDiffPercent20, dayCnt, curStatus, maxVolumePercent])
    
    file_result.write(code + "    ")
    file_result.write(str(maDiffPercent5) + "    ")
    file_result.write(str(maDiffPercent10) + "    ")
    file_result.write(str(maDiffPercent20) + "    ")
    file_result.write("\n")
    
file_csv.close()
file_result.close()
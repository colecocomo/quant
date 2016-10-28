# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:22:39 2016

@author: colec
"""

import tushare as ts
import csv

stockID = '002219'

file_csv = open(stockID + 'TodayTicks.csv', 'wb+')
spamwriter = csv.writer(file_csv,dialect='excel')
spamwriter.writerow(['time', 'price', 'pchange', 'change', 'volume', 'amount', 'type'])

fileHistory_csv = open(stockID + 'HistoryTicks.csv', 'wb+')
spamwriterHistory = csv.writer(fileHistory_csv,dialect='excel')
spamwriterHistory.writerow(['time', 'price', 'change', 'volume', 'amount', 'type'])

df = ts.get_today_ticks('002219')
dfHistory = ts.get_tick_data('002219', date='2016-08-16')
total = 0
neutral = 0
for indexH, rowH in dfHistory.iterrows():
    #print(rowH[5])
    spamwriterHistory.writerow([rowH[0], rowH[1], rowH[2], rowH[3], rowH[4], rowH[5].decode('utf-8').encode('gb2312')])
    
for index, row in df.iterrows():
    print(row[6])
    spamwriter.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6].encode('gbk')])
    if row[6] == '买盘'.decode('utf-8'):
        total += row[5]
    if row[6] == '卖盘'.decode('utf-8'):
        total -= row[5]
    else:
        neutral += row[5]
print("total:" + str(total) + "neutral:" + str(neutral))

df1 =ts.get_tick_data('002219',date='2016-09-28')
total1 = 0
neutral1 = 0
for index1, row1 in df1.iterrows():
    if row1[5] == '买盘'.decode('utf-8'):
        total1 += row1[4]
    if row1[5] == '卖盘'.decode('utf-8'):
        total1 -= row1[4]
    else:
        neutral1 += row[5]
print("total1:" + str(total1) + "neutral1:" + str(neutral1 / 10000))
#print(df)
#df.to_excel(writer)
#dd = ts.get_sina_dd('002219', date='2016-07-12')
#print(dd)
#hold = ts.fund_holdings(2016, 1)
#print(hold)
#forecast = ts.forecast_data(2016,3)
file_csv.close()
fileHistory_csv.close()
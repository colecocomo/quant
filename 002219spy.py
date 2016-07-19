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

df = ts.get_today_ticks('002219')
total = 0
neutral = 0
for index, row in df.iterrows():
    print(row[6].decode('ascii').encode('gb2312'))
    spamwriter.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6].decode('utf-8').encode('gb2312')])
    if row[6] == '买盘'.decode('utf-8'):
        total += row[5]
    if row[6] == '卖盘'.decode('utf-8'):
        total -= row[5]
    else:
        neutral += row[5]
print("total:" + str(total) + "neutral:" + str(neutral))

df1 =ts.get_tick_data('002219',date='2016-07-18')
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
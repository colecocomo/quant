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
for index, row in df.iterrows():
    spamwriter.writerow([row[0], row[1], row[2], row[3]])
#print(df)
#df.to_excel(writer)
dd = ts.get_sina_dd('002219', date='2016-07-12')
print(dd)
hold = ts.fund_holdings(2016, 1)
print(hold)
forecast = ts.forecast_data(2016,3)
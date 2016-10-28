# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:17:29 2016

@author: colec
"""

import tushare as ts
import csv
import codecs

preDivi_csv = codecs.open('PreDiviResult.csv', 'wb+', 'utf-8')
spamwriter = csv.writer(preDivi_csv,dialect='excel')
spamwriter.writerow(['stock', 'name', 'year', 'report_date', "divi", "shares"])

df = ts.profit_data(top=1000, year=2016)
for code, stockRow in df.iterrows():
    print("pre divi " + stockRow['code'])
    print(type(stockRow['shares']))
    spamwriter.writerow([stockRow['code'], stockRow['name'], 
                         stockRow['year'], stockRow['report_date'], 
                         stockRow["divi"], 
                         stockRow["shares"]])
                      
preDivi_csv.close()


preEarning_csv = open('PreEarningResult.csv', 'wb+')
spamwriter1 = csv.writer(preEarning_csv,dialect='excel')
spamwriter1.writerow(['stock', 'name', 'type', 'report_date', "pre_eps", "range"])

tmp = str('111')
print(tmp.decode('utf-8').encode('gb2312'))
df1 = ts.forecast_data(2016,3)
for code1, stockRow1 in df1.iterrows():
    print("pre earning " + stockRow1['code'])
    print("name type " + type(stockRow1['name']).__name__)
    print("type type " + type(stockRow1['type']).__name__)
    print("pre_eps type " + type(stockRow1['pre_eps']).__name__)
    print(stockRow1['range'])
    print("range type " + type(stockRow1['range']).__name__)
    spamwriter1.writerow([stockRow1['code'], stockRow1['name'], 
                         stockRow1['type'].encode('gb2312'), stockRow1['report_date'], 
                         stockRow1["pre_eps"], 
                            tmp.decode('utf-8').encode('gb2312')])
                      
preEarning_csv.close()
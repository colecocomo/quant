# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 14:41:27 2016

@author: colec
"""

import tushare as ts
import csv

file_csv = open('AreaStatistic.csv', 'wb+')
spamwriter = csv.writer(file_csv,dialect='excel')
spamwriter.writerow(['code', 'name', 'area'])

all_stock = ts.get_area_classified()

for code, stockRow in all_stock.iterrows():
    areaName = str(stockRow["area"])
    if (areaName.find("天津") != -1):
        spamwriter.writerow([code, stockRow["name"].decode('utf-8').encode('gb2312'), stockRow["area"].decode('utf-8').encode('gb2312')])
        
file_csv.close()
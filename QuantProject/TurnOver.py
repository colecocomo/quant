# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:22:39 2016

@author: colec
"""

import tushare as ts
import pandas as pd
import time

allStock = ts.get_stock_basics()

endTime = time.localtime(time.time() - 0)
formatEndTime = time.strftime("%Y-%m-%d", endTime)

dates = pd.bdate_range(end=formatEndTime, periods=5, freq="B")
datesList = dates.tolist()

for code, stockRow in allStock.iterrows():
    for var in datesList:
        date = str(var)[0:10]
        stockInfo = ts.get_h_data(code, start=date, end=date)
        print (stockInfo)
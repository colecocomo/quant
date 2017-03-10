# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:22:39 2016

@author: colec
"""

import tushare as ts

stockID = '002222'

# df = ts.get_today_ticks(stockID)
df = ts.get_tick_data(stockID, date='2016-11-23')
_totalCnt = 0
_totalCost = 0
_close = 0
for index, row in df.iterrows():
    # print (row)
    if _close == 0:
        _close = float(row[1])
    _price = float(row[1])
    _cnt = int(row[4])

    _totalCnt += _cnt * 100
    _totalCost += _price * _cnt * 100

_avgPrice = _totalCost / _totalCnt
_diffPercent = (_close - _avgPrice) / _avgPrice
print("Avg price is:" + str(_avgPrice) + " diffPercent is:" + str(_diffPercent * 100))

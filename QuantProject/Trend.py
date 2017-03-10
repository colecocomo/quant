# -*- coding: utf-8 -*-
"""
Created on Mar. 6 11:15:39 2017

@author: cole
"""

import tushare as ts
import pandas as pd
import time
import csv


def floatToStr(value, num):
    """

    :param value:
    :return:
    """
    return ("%." + str(num) + "f") % value


file_csv = open('Trend.csv', 'wb+')
spam_writer = csv.writer(file_csv, dialect='excel')
spam_writer.writerow(['code'])

TrendNone = 0
TrendUp = 1
TrendDown = 2

allStock = ts.get_stock_basics()

endTime = time.localtime(time.time() - 86400)
formatEndTime = time.strftime("%Y-%m-%d", endTime)
periodsNum = 30
dates = pd.bdate_range(end=formatEndTime, periods=periodsNum, freq="B")
datesList = dates.tolist()

for code, stockRow in allStock.iterrows():
    stockInfo = ts.get_k_data(code,
                              start=str(datesList[0])[0:10],
                              end=str(datesList[periodsNum-1])[0:10])
    _isFirst = True
    _lastClose = 0.0
    _trend = TrendNone
    _oldTrend = TrendNone
    _trendBegin = 0.0
    _trendTmp = 0.0
    _closeAmplitudePercent = 0.0
    for idx, infoRow in stockInfo.iterrows():
        close = float(infoRow[2])
        high = float(infoRow[3])
        low = float(infoRow[4])

        if _isFirst:
            _isFirst = False
            _lastClose = close
            _trendBegin = close
        else:
            _closeAmplitudePercent = (close - _lastClose) / _lastClose
            if _closeAmplitudePercent > 0.000001:
                _trend = TrendUp
            elif _closeAmplitudePercent < -0.00001:
                _trend = TrendDown

        if _oldTrend == TrendNone:
            _oldTrend = _trend
            _trendBegin = _lastClose

        if _oldTrend != _trend:
            if _oldTrend == TrendUp:
                if close < _trendBegin:
                    _oldTrend = _trend
            if _oldTrend == TrendDown:
                _oldTrend = _trend



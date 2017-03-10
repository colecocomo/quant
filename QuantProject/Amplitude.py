# -*- coding: utf-8 -*-
"""
Created on Mar. 6 11:15:39 2017

@author: cole
"""

import tushare as ts
import pandas as pd
import time
import csv
import math


def floatToStr(value, num):
    """

    :param value:
    :return:
    """
    return ("%." + str(num) + "f") % value


file_csv = open('Amplitude.csv', 'wb+')
spam_writer = csv.writer(file_csv,dialect='excel')
spam_writer.writerow(['code', 'hightAmplitude', 'lowAmplitude', 'totalAmplitude', 'totalDay', 'continueLimitUp'])

allStock = ts.get_stock_basics()

endTime = time.localtime(time.time() - 86400)
formatEndTime = time.strftime("%Y-%m-%d", endTime)
periodsNum = 60
dates = pd.bdate_range(end=formatEndTime, periods=periodsNum, freq="B")
datesList = dates.tolist()

for code, stockRow in allStock.iterrows():
    try:
        stockInfo = ts.get_k_data(code,
                                  start=str(datesList[0])[0:10],
                                  end=str(datesList[periodsNum - 1])[0:10])
    except Exception, e:
        try:
            stockInfo = ts.get_k_data(code,
                                      start=str(datesList[0])[0:10],
                                      end=str(datesList[59])[0:10])
        except Exception, e:
            continue
    _count = 0
    _highAmplitudePercent = 0.0
    _lowAmplitudePercent = 0.0
    _highAmplitudePercentStr = "0.00"
    _lowAmplitudePercentStr = "0.00"
    _totalAmplitudePercent = 0.0
    _totalAmplitudePercentStr = "0.0"
    _totalAmplitudePercentM = 0.0
    _totalAmplitudePercentL = 0.0
    _lastClose = 0.0
    _continueLimitUp = 0
    _isFirst = True
    _closeAmplitudePercent = 0.0
    for idx, infoRow in stockInfo.iterrows():
        _count += 1
        close = float(infoRow[2])
        high = float(infoRow[3])
        low = float(infoRow[4])

        if _isFirst:
            _isFirst = False
            _lastClose = close
        else:
            _closeAmplitudePercent = (close - _lastClose) / _lastClose
            _closeAmplitudePercent = math.fabs(_closeAmplitudePercent)
            _lastClose = close

        if _closeAmplitudePercent > 0.0980000:
            _continueLimitUp += 1
        else:
            _continueLimitUp = 0

        _highAmplitudePercent += ((high - close) / close)
        _lowAmplitudePercent += ((close - low) / close)
        __tmp = (high - low) / close
        if (__tmp > 0.02) and (__tmp < 0.05):
            _totalAmplitudePercentM += __tmp
        if __tmp > 0.05:
            _totalAmplitudePercentL += __tmp
        _totalAmplitudePercent += __tmp

    if _count > 5:
        _highAmplitudePercent /= _count
        _highAmplitudePercent *= 100
        _lowAmplitudePercent /= _count
        _lowAmplitudePercent *= 100
        _highAmplitudePercentStr = floatToStr(_highAmplitudePercent, 2)
        _lowAmplitudePercentStr = floatToStr(_lowAmplitudePercent, 2)
        _totalAmplitudePercent += (_totalAmplitudePercentM  + _totalAmplitudePercentL)
        _totalAmplitudePercent /= _count
        _totalAmplitudePercent *= 100
        _totalAmplitudePercentStr = floatToStr(_totalAmplitudePercent, 2)
    spam_writer.writerow([code, _highAmplitudePercentStr, _lowAmplitudePercentStr,
                          _totalAmplitudePercentStr, str(_count), str(_continueLimitUp)])
    print "statistic " + code + ' ' + _highAmplitudePercentStr + ' ' + \
          _lowAmplitudePercentStr + ' ' + _totalAmplitudePercentStr + ' ' + \
          str(_count) + ' ' + str(_continueLimitUp)

file_csv.close()

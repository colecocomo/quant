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


file_csv = open('Trend.csv', 'wb+')
spam_writer = csv.writer(file_csv, dialect='excel')
spam_writer.writerow(['code'])

TrendNone = 0
TrendUp = 1
TrendDown = 2
TrendStringDic = {TrendNone: "无", TrendUp: "Up", TrendDown: "Down"}

allStock = ts.get_stock_basics()

endTime = time.localtime(time.time() - 86400)
formatEndTime = time.strftime("%Y-%m-%d", endTime)
periodsNum = 120
dates = pd.bdate_range(end=formatEndTime, periods=periodsNum, freq="B")
datesList = dates.tolist()

for code, stockRow in allStock.iterrows():
    print code
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
    _trendList = []
    _trendDay = 0
    for idx, infoRow in stockInfo.iterrows():
        close = float(infoRow[2])
        high = float(infoRow[3])
        low = float(infoRow[4])
        _trendDay += 1

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
            _trendPoint = {"TrendType": TrendStringDic[_oldTrend], "TrendBegin": _trendBegin,
                           "TrendEnd": _lastClose, "TrendDay": _trendDay,
                           "TrendPercent": floatToStr(((_lastClose - _trendBegin) * 100 / _trendBegin), 2) + "%"}
            _trendList.append(_trendPoint)

            _trendBegin = _lastClose
            _oldTrend = _trend
            _trendDay = 0
        else:
            _lastClose = close

    print "begin: " + str(_trendList.__len__())
    print _trendList
    _iterIdx = 0
    while (_iterIdx < _trendList.__len__() - 1) and (_trendList.__len__() > 1):
        _trendTmp1 = _trendList[_iterIdx]
        _trendTmp2 = _trendList[_iterIdx + 1]

        _trendTmpBegin1 = _trendTmp1["TrendBegin"]
        _trendTmpEnd1 = _trendTmp1["TrendEnd"]
        _trendTmpDay1 = _trendTmp1["TrendDay"]
        _trendTmpType1 = _trendTmp1["TrendType"]
        _trendTmpPercent1 = (_trendTmpEnd1 - _trendTmpBegin1) / _trendTmpBegin1

        _trendTmpBegin2 = _trendTmp2["TrendBegin"]
        _trendTmpEnd2 = _trendTmp2["TrendEnd"]
        _trendTmpDay2 = _trendTmp2["TrendDay"]
        _trendTmpType2 = _trendTmp2["TrendType"]
        _trendTmpPercent2 = (_trendTmpEnd2 - _trendTmpBegin2) / _trendTmpBegin2

        if math.fabs(_trendTmpPercent1) < 0.050000:
            if math.fabs(_trendTmpPercent1) < math.fabs(_trendTmpPercent2):
                _trendList[_iterIdx + 1] = {"TrendType": _trendTmpType2,
                                            "TrendBegin": _trendTmpBegin1,
                                            "TrendEnd": _trendTmpEnd2,
                                            "TrendDay": (_trendTmpDay1 + _trendTmpDay2),
                                            "TrendPercent":
                                                floatToStr(((_trendTmpEnd2 - _trendTmpBegin1) * 100 / _trendTmpBegin1),
                                                           2) + "%"}
                del _trendList[_iterIdx]
            else:
                _trendList[_iterIdx] = {"TrendType": _trendTmpType1,
                                        "TrendBegin": _trendTmpBegin1,
                                        "TrendEnd": _trendTmpEnd2,
                                        "TrendDay": (_trendTmpDay1 + _trendTmpDay2),
                                        "TrendPercent":
                                            floatToStr(((_trendTmpEnd2 - _trendTmpBegin1) * 100 / _trendTmpBegin1),
                                                       2) + "%"}
                del _trendList[_iterIdx + 1]

            _iterIdx = 0
        #elif math.fabs(_trendTmpPercent2) < 0.050000:
        #    _trendList[_iterIdx] = {"TrendType": _trendTmpType1,
        #                            "TrendBegin": _trendTmpBegin1,
        #                            "TrendEnd": _trendTmpEnd2,
        #                            "TrendDay": (_trendTmpDay1 + _trendTmpDay2),
        #                            "TrendPercent":
        #                                floatToStr(((_trendTmpEnd2 - _trendTmpBegin1) * 100 / _trendTmpBegin1),
        #                                           2) + "%"}
        #    del _trendList[_iterIdx + 1]
        #    _iterIdx -= 1
        else:
            _iterIdx += 1
    print "end: " + str(_trendList.__len__())
    print _trendList





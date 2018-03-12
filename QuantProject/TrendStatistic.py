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
import re


def floatToStr(value, num):
    """

    :param value:
    :return:
    """
    return ("%." + str(num) + "f") % value


file_csv = open('TrendStatistic.csv', 'wb+')
spam_writer = csv.writer(file_csv, dialect='excel')
spam_writer.writerow(['code', 'mask', 'detail', "growth"])

TrendNone = 0
TrendUp = 1
TrendDown = 2
TotalQuarter = 4
TrendStringDic = {TrendNone: "无", TrendUp: "Up", TrendDown: "Down"}

allStock = ts.get_stock_basics()

endTime = time.localtime(time.time() - 0)
formatEndTime = time.strftime("%Y-%m-%d", endTime)
periodsNum = 120
CombineSlice = 0.050000
dates = pd.bdate_range(end=formatEndTime, periods=periodsNum, freq="B")
datesList = dates.tolist()

yearNow = int(formatEndTime[0:4])
monthNow = int(formatEndTime[5:7])
curQuarter = int(monthNow / 4) + 1

quarterIdx = 0
yearList = [0, 0, 0, 0]
quarterList = [0, 0, 0, 0]
growthList = [0, 0, 0, 0]
while quarterIdx < TotalQuarter:
    print str(yearNow) + "-" + str(curQuarter)
    try:
        _growth = ts.get_growth_data(yearNow, curQuarter)
    except Exception, e:
        try:
            _growth = ts.get_growth_data(yearNow, curQuarter)
        except Exception, e1:
            if curQuarter == 1:
                yearNow -= 1
                curQuarter = 4
            else:
                curQuarter -= 1
            continue
    if _growth is None:
        if curQuarter == 1:
            yearNow -= 1
            curQuarter = 4
        else:
            curQuarter -= 1
        continue
    else:
        _growth.fillna(0)
        yearList[quarterIdx] = yearNow
        quarterList[quarterIdx] = curQuarter
        growthList[quarterIdx] = _growth.copy()
        # print growthList[quarterIdx].head(10)
        quarterIdx += 1
        if curQuarter == 1:
            yearNow -= 1
            curQuarter = 4
        else:
            curQuarter -= 1
        # print '------------new---line----------------------'
# print yearList
# print quarterList

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
    _trendList = []
    _trendDay = 0
    for idx, infoRow in stockInfo.iterrows():
        close = float(infoRow[2])
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
                           "TrendPercent": ((_lastClose - _trendBegin) * 100 / _trendBegin),
                           "TrendPercentStr": floatToStr(((_lastClose - _trendBegin) * 100 / _trendBegin), 2) + "%"}
            _trendList.append(_trendPoint)

            _trendBegin = _lastClose
            _oldTrend = _trend
            _trendDay = 0
        else:
            _lastClose = close

    print "begin: " + str(_trendList.__len__())
    # print _trendList
    _iterIdx = 0
    _combineMask = CombineSlice
    if _trendList.__len__() > 8:
        while _trendList.__len__() > 8:
            _iterIdx = 0
            while _iterIdx < _trendList.__len__() - 1:
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

                if math.fabs(_trendTmpPercent1) < _combineMask:
                    if math.fabs(_trendTmpPercent1) < math.fabs(_trendTmpPercent2):
                        _trendList[_iterIdx + 1] = {"TrendType": _trendTmpType2,
                                                    "TrendBegin": _trendTmpBegin1,
                                                    "TrendEnd": _trendTmpEnd2,
                                                    "TrendDay": (_trendTmpDay1 + _trendTmpDay2),
                                                    "TrendPercent": ((_trendTmpEnd2 - _trendTmpBegin1) * 100 / _trendTmpBegin1),
                                                    "TrendPercentStr":
                                                        floatToStr(((_trendTmpEnd2 - _trendTmpBegin1) * 100 / _trendTmpBegin1),
                                                                   2) + "%"}
                        del _trendList[_iterIdx]
                    else:
                        _trendList[_iterIdx] = {"TrendType": _trendTmpType1,
                                                "TrendBegin": _trendTmpBegin1,
                                                "TrendEnd": _trendTmpEnd2,
                                                "TrendDay": (_trendTmpDay1 + _trendTmpDay2),
                                                "TrendPercent": ((_trendTmpEnd2 - _trendTmpBegin1) * 100 / _trendTmpBegin1),
                                                "TrendPercentStr":
                                                    floatToStr(((_trendTmpEnd2 - _trendTmpBegin1) * 100 / _trendTmpBegin1),
                                                               2) + "%"}
                        del _trendList[_iterIdx + 1]

                    _iterIdx = 0
                # elif math.fabs(_trendTmpPercent2) < _combineMask:
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
            _combineMask += CombineSlice
            print "_combineMask is: " + str(_combineMask)
    print "end: " + str(_trendList.__len__())
    # print _trendList
    _iterIdx = 0
    _mask = 0L
    _lastTrendPercent = 0
    _lastTrendMask = 0
    _detailStr = ''
    while _iterIdx < _trendList.__len__():
        _trendValue = _trendList[_iterIdx]
        _percent = _trendValue["TrendPercent"]
        _detailStr += (_trendValue["TrendType"] + ' ' +
                       _trendValue["TrendPercentStr"] + ' ' +
                       str(_trendValue["TrendBegin"]) + ' ' +
                       str(_trendValue["TrendEnd"]) + '\r\n')

        if _isFirst:
            if _percent > 0.001:
                _lastTrendMask = TrendUp
            elif _percent < -0.001:
                _lastTrendMask = TrendDown
            _lastTrendPercent = TrendDown
            _mask = _mask * math.pow(10, 1) + _lastTrendMask
            _isFirst = False
        else:
            if math.fabs(_percent) < (math.fabs(_lastTrendPercent) * 0.3):
                _mask = _mask * math.pow(10, 1) + _lastTrendMask
            else:
                if _percent > 0.001:
                    _lastTrendMask = TrendUp
                elif _percent < -0.001:
                    _lastTrendMask = TrendDown
                _mask = _mask * math.pow(10, 1) + _lastTrendMask
            _lastTrendPercent = _percent

        _iterIdx += 1
    if re.match("^.{4,}", str(int(_mask))):
        if re.match("^.*1{3,}$", str(int(_mask))):
            print str(code) + "\'s valid mask is: " + str(int(_mask))
        else:
            print "Invalid trend mask: " + str(int(_mask))
            continue
    else:
        print "Invalid trend mask: " + str(int(_mask))
        continue

    _quarterIdx = 0
    _growthStr = ""
    while _quarterIdx < TotalQuarter:
        _isFind = False
        for idx, growthRow in growthList[_quarterIdx].iterrows():
            if growthRow[0] == code:
                _growthStr += (str(yearList[_quarterIdx]) + "-" +
                               str(quarterList[_quarterIdx]) + ": " +
                               "mbrg: " + str(growthRow[2]) + "% " +
                               "nprg: " + str(growthRow[3]) + "% " +
                               "epsg: " + str(growthRow[6]) + "% " + '\r\n')
                _isFind = True
                break
        if not _isFind:
            _growthStr += (str(yearList[_quarterIdx]) + "-" +
                           str(quarterList[_quarterIdx]) + ": " +
                           "mbrg: unknown   " +
                           "nprg: unknown   " +
                           "epsg: unknown   " + '\r\n')
        _quarterIdx += 1

    spam_writer.writerow([code, _mask, _detailStr, _growthStr])


file_csv.close()







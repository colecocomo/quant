# -*- coding: utf-8 -*-
"""
Created on Mar. 23 13:49:39 2017

@author: cole
"""

import tushare as ts
import requests as req
import time
import os

requestUrl_SJS = "http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=" + \
             "7&AJAX=AJAX-TRUE&CATALOGID=sgshqd&TABKEY=tab1&tab1PAGENUM="
downloadLinkPre_SJS = "http://www.szse.cn"
downloadKeyword_SJS = "\"window.open(\'"
encodeKeyword_SJS = "\'+encodeURIComponent(\'"
downloadEnd_SJS = "\'))\"><img"

pageIdx = 1
curTime = time.localtime(time.time())
formatCurTime = ""
if curTime.tm_hour >= 16:
    formatCurTime = time.strftime("%Y%m%d", curTime)
else:
    formatCurTime = time.strftime("%Y%m%d", time.localtime(time.time() - 0))
print formatCurTime
isCurDay = True
if os.path.exists(".\\" + formatCurTime):
    # os.remove(".\\" + formatCurTime)
    isCurDay = True
else:
    os.mkdir(".\\" + formatCurTime)
while isCurDay:
    _pageContent = req.get(requestUrl_SJS + str(pageIdx))
    _contentDetail = _pageContent.text
    _downloadKeywordIdx = _contentDetail.find(downloadKeyword_SJS)
    while -1 != _downloadKeywordIdx:
        _downloadKeywordIdx += downloadKeyword_SJS.__len__()
        _contentDetail = _contentDetail[_downloadKeywordIdx:]
        _encodeKeywordIdx = _contentDetail.find(encodeKeyword_SJS)
        _contentDetailFileName = _contentDetail[(_encodeKeywordIdx + encodeKeyword_SJS.__len__()):]
        _endIdx = _contentDetailFileName.find(downloadEnd_SJS)
        _fileName = _contentDetailFileName[:_endIdx]
        _fileNameArray = _fileName.split(";")
        _fileDateTime = _fileNameArray[0].split("_")[2]
        if _fileDateTime != formatCurTime:
            isCurDay = False
            break
        _downloadLinkStr = (downloadLinkPre_SJS + _contentDetail[:_encodeKeywordIdx] +
                            _fileNameArray[0] + "%3B" + _fileNameArray[1])
        print _downloadLinkStr
        _rsp = req.get(_downloadLinkStr)
        print _rsp
        if _rsp.status_code == 200:
            with open(".\\" + formatCurTime + "\\" + _fileNameArray[0] + ".txt", 'wb') as f:
                f.write(_rsp.content)
        _contentDetail = _contentDetailFileName[(_endIdx + downloadEnd_SJS.__len__()):]
        _downloadKeywordIdx = _contentDetail.find(downloadKeyword_SJS)
    pageIdx += 1


pcfFile = open("pcf_159931_20170329.txt", "r")
lineStr = pcfFile.readline()
isComponent = False
creationRedemptionUnit = 0
componentID = []
componentNumDic = {}
componentSubstituteFlagDic = {}
componentPremiumRatioDic = {}
componentCashDic = {}
while lineStr:
    if lineStr.find("CreationRedemptionUnit") != -1:
        tmpArray = lineStr.split('=')
        # print tmpArray
        creationRedemptionUnit = float(tmpArray[1])

    if lineStr.find("RECORDEND") != -1:
        isComponent = False

    if isComponent:
        componentArray = lineStr.split('|')
        # print componentArray
        securityID = componentArray[1]
        componentID.append(securityID)
        componentNumDic[securityID] = componentArray[3]
        componentSubstituteFlagDic[securityID] = componentArray[4]
        componentPremiumRatioDic[securityID] = componentArray[5]
        componentCashDic[securityID] = componentArray[6]

    if lineStr.find("RECORDBEGIN") != -1:
        isComponent = True

    lineStr = pcfFile.readline()

"""
print "componentID=========="
print componentID
print "creationRedemptionUnit=========="
print creationRedemptionUnit
print "componentNumDic=========="
print componentNumDic
print "componentSubstituteFlagDic=========="
print componentSubstituteFlagDic
print "componentPremiumRatioDic=========="
print componentPremiumRatioDic
print "componentCashDic=========="
print componentCashDic
"""

while True:
    _totalCost = .0
    for componentIdx in componentID:
        if componentSubstituteFlagDic[componentIdx] == "2":
            # print str(componentIdx) + "cash is: " + componentCashDic[componentIdx]
            _totalCost += float(componentCashDic[componentIdx])
        else:
            tickData = ts.get_realtime_quotes(componentIdx)
            price = float(tickData.iloc[0][3])
            '''
            print str(componentIdx) + " Price is: " + str(price) + " Num is: " + \
                componentNumDic[componentIdx] + " Total is: " + \
                str(price * int(componentNumDic[componentIdx]))
            '''
            _totalCost += (price * int(componentNumDic[componentIdx]))
    _price1 = _totalCost / creationRedemptionUnit
    _tmp = ts.get_realtime_quotes("159931")
    _price2 = _tmp.iloc[0][3]
    print "Price1 is: " + str(_price1) + " | Price2 is: " + str(_price2)

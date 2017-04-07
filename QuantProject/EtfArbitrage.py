# -*- coding: utf-8 -*-
"""
Created on Mar. 23 13:49:39 2017

@author: cole
"""

import tushare as ts
import requests as req
import time
import os
from xml.dom.minidom import parse
import xml.dom.minidom


class EtfInfo(object):

    """
    ETF 申购/赎回清单
    """

    def __init__(self, etf_name, etf_code, creation_redemption_unit, component_id,
                 component_num_dic, component_substitute_flag_dic,
                 component_premium_ratio_dic, component_cash_dic):
        """

        :param etf_name: 名称
        :param etf_code: 代码
        :param creation_redemption_unit: 申购/赎回最小单位
        :param component_id: 成份股指
        :param component_num_dic: 成份股指数量
        :param component_substitute_flag_dic: 现金替代标志
        :param component_premium_ratio_dic: 现金替代浮动比率
        :param component_cash_dic: 申购/赎回金额
        """
        self.etfName = etf_name
        self.etfCode = etf_code
        self.creationRedemptionUnit = creation_redemption_unit
        self.componentID = []
        self.componentID.extend(component_id)
        self.componentNumDic = {}
        self.componentNumDic.update(component_num_dic)
        self.componentSubstituteFlagDic = {}
        self.componentSubstituteFlagDic.update(component_substitute_flag_dic)
        self.componentPremiumRatioDic = {}
        self.componentPremiumRatioDic.update(component_premium_ratio_dic)
        self.componentCashDic = {}
        self.componentCashDic.update(component_cash_dic)


requestUrl_SJS = "http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=" + \
             "7&AJAX=AJAX-TRUE&CATALOGID=sgshqd&TABKEY=tab1&tab1PAGENO="
downloadLinkPre_SJS = "http://www.szse.cn"
downloadKeyword_SJS = "\"window.open(\'"
encodeKeyword_SJS = "\'+encodeURIComponent(\'"
downloadEnd_SJS = "\'))\"><img"
requestUrl_SHJS = "http://www.sse.com.cn/disclosure/fund/etflist/"
tmp = "http://query.sse.com.cn/infodisplay/queryETFNewAllInfo.do"
tmp1 = {"isPagination": True,
        "type": 6,
        "pageHelp.pageSize": 25,
        "pageHelp.pageCount": 50,
        "pageHelp.pageNo": 1,
        "pageHelp.beginPage": 1,
        "pageHelp.cacheSize": 1,
        "pageHelp.endPage": 5}

headers1 = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Cookie': "",
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}
# _tmp1 = req.get(requestUrl_SHJS, headers=headers1)
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Cookie': "",
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Host': 'query.sse.com.cn',
    'Referer': 'http://www.sse.com.cn/disclosure/fund/etflist/'
}
# _tmp = req.get(tmp, data=json.dumps(tmp1), headers=headers)

pageIdx = 1
curTime = time.localtime(time.time())
formatCurTime = ""
if curTime.tm_hour >= 15:
    formatCurTime = time.strftime("%Y%m%d", curTime)
else:
    formatCurTime = time.strftime("%Y%m%d", time.localtime(time.time() - 86400))
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
    print "pageidx: " + str(pageIdx)

EtfList = []
if os.path.exists(".\\" + formatCurTime):
    _fileList = os.listdir(".\\" + formatCurTime)
    for i in range(0, _fileList.__len__()):
        _filePath = os.path.join(".\\" + formatCurTime + "\\", _fileList[i])
        if os.path.isfile(_filePath):
            _pcfFile = open(_filePath, "r")
            _isSHJS = (_filePath.find(".ETF") != -1)
            _lineStr = _pcfFile.readline()
            _isXml = (_lineStr.find("<?xml") != -1)

            _creationRedemptionUnit = 0
            _isComponent = False
            _etfName = ""
            _etfCode = 0
            _componentID = []
            _componentNum = 0
            _componentNumDic = {}
            _componentSubstituteFlagDic = {}
            _componentPremiumRatioDic = {}
            _componentCashDic = {}

            # 解析深交所xml格式的pcf文件
            if not _isSHJS and _isXml:
                _pcfFile.close()
                _DOMTree = xml.dom.minidom.parse(_filePath)
                _data = _DOMTree.documentElement

                _componentNum = int(_data.getElementsByTagName("RecordNum")[0].childNodes[0].data)
                if _componentNum == 1:
                    continue

                _etfName = _data.getElementsByTagName("Symbol")[0].childNodes[0].data
                _etfCode = _data.getElementsByTagName("SecurityID")[0].childNodes[0].data
                _creationRedemptionUnit = float(_data.getElementsByTagName(
                    "CreationRedemptionUnit")[0].childNodes[0].data)

                _componentContainer = _data.getElementsByTagName("Component")
                for _componentContainerIdx in _componentContainer:
                    _securityID = _componentContainerIdx.getElementsByTagName(
                        "UnderlyingSecurityID")[0].childNodes[0].data
                    _componentID.append(_securityID)
                    _componentSubstituteFlagDic[_securityID] = _componentContainerIdx.getElementsByTagName(
                        "SubstituteFlag")[0].childNodes[0].data
                    _tmpCash = 0
                    _tmpRatio = 0
                    _tmpShare = 0
                    if _componentSubstituteFlagDic[_securityID] == "2":
                        _tmpCash = _componentContainerIdx.getElementsByTagName(
                            "CreationCashSubstitute")[0].childNodes[0].data
                    elif _componentSubstituteFlagDic[_securityID] == "1":
                        _tmpRatio = _componentContainerIdx.getElementsByTagName(
                            "PremiumRatio")[0].childNodes[0].data
                        _tmpShare = _componentContainerIdx.getElementsByTagName(
                            "ComponentShare")[0].childNodes[0].data
                    _componentPremiumRatioDic[_securityID] = _tmpRatio
                    _componentNumDic[_securityID] = _tmpShare
                    _componentCashDic[_securityID] = _tmpCash

                EtfList.append(EtfInfo(_etfName, _etfCode, _creationRedemptionUnit, _componentID,
                                       _componentNumDic, _componentSubstituteFlagDic,
                                       _componentPremiumRatioDic, _componentCashDic))

            # 解析深交所txt格式的pcf文件
            _isMMF = False  # 是否是货币基金etf
            if not _isSHJS and not _isXml:
                while _lineStr:
                    if _lineStr.find("CreationRedemptionUnit") != -1:
                        _tmpArray = _lineStr.split('=')
                        # print tmpArray
                        _creationRedemptionUnit = float(_tmpArray[1])

                    if _lineStr.find("TotalRecordNum=") != -1:
                        _tmpArray = _lineStr.split('=')
                        _componentNum = int(_tmpArray[1])
                        if _componentNum == 1:
                            _isMMF = True
                            break

                    if _lineStr.find("FundID=") != -1:
                        _tmpArray = _lineStr.split('=')
                        _etfCode = _tmpArray[1]

                    if _lineStr.find("FundName=") != -1:
                        _tmpArray = _lineStr.split('=')
                        _etfName = _tmpArray[1]

                    if _lineStr.find("RECORDEND") != -1:
                        _isComponent = False

                    if _isComponent:
                        _componentArray = _lineStr.split('|')
                        # print componentArray
                        _securityID = _componentArray[1]
                        _componentID.append(_securityID)
                        _componentNumDic[_securityID] = _componentArray[3]
                        _componentSubstituteFlagDic[_securityID] = _componentArray[4]
                        _componentPremiumRatioDic[_securityID] = _componentArray[5]
                        _componentCashDic[_securityID] = _componentArray[6]

                    if _lineStr.find("RECORDBEGIN") != -1:
                        _isComponent = True

                    _lineStr = _pcfFile.readline()
                if not _isMMF:
                    EtfList.append(EtfInfo(_etfName, _etfCode, _creationRedemptionUnit, _componentID,
                                           _componentNumDic, _componentSubstituteFlagDic,
                                           _componentPremiumRatioDic, _componentCashDic))
                _pcfFile.close()

while True:
    for etfIdx in EtfList:
        _totalCost = .0
        for _componentIdx in etfIdx.componentID:
            if etfIdx.componentSubstituteFlagDic[_componentIdx] == "2":
                # print str(componentIdx) + "cash is: " + componentCashDic[componentIdx]
                _totalCost += float(etfIdx.componentCashDic[_componentIdx])
            else:
                tickData = ts.get_realtime_quotes(_componentIdx)
                price = float(tickData.iloc[0][3])
                '''
                print str(componentIdx) + " Price is: " + str(price) + " Num is: " + \
                    componentNumDic[componentIdx] + " Total is: " + \
                    str(price * int(componentNumDic[componentIdx]))
                '''
                _totalCost += (price * float(etfIdx.componentNumDic[_componentIdx]))
        _price1 = _totalCost / etfIdx.creationRedemptionUnit
        _tmp = ts.get_realtime_quotes(_componentIdx)
        _price2 = _tmp.iloc[0][3]
        print (etfIdx.etfName + "(" + etfIdx.etfCode + ")" + " Price1 is: " + str(_price1) +
               " | Price2 is: " + str(_price2))

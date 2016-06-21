# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tushare as ts
import time
import string

def logError(str):
    file_error = open("error.txt", "a+")
    file_error.write(str)
    file_error.write("\n")
    file_error.close()

def stockBelongs(id):
    if(id[0:2] == "60"):
        return "000001"
    elif(id[0:2] == "00"):
        return "399001"
    elif(id[0:2] == "30"):
        return "399006"
    else:
        logError("未知股票市场id：" + id)
        return "0"

def belongToHist(dayValue, dayIdx, id):
    while(True):
        preTime = time.localtime(time.time() - dayValue[dayIdx] * 86400)
        formatPreTime = time.strftime("%Y-%m-%d", preTime)
        history = ts.get_h_data(id, \
                            start = formatPreTime, \
                            end = formatPreTime, \
                            pause=0.01, \
                            index = True)
        if (history is None or history.empty):
            print(formatPreTime + "休市")
            dayValue[dayIdx] += 1
            continue 
        return history
        
def timeRegion(timeValue, regionNum, timeDict):
    timeIdx = 0
    endTimeIdx = 1
    while(True):
        endTime = time.localtime(time.time() - endTimeIdx * 86400)
        formatEndTime= time.strftime("%Y-%m-%d", endTime)
        history = ts.get_h_data("000001", \
                                start = formatEndTime, \
                                end = formatEndTime, \
                                index = True)
        if (history is None or history.empty):
            print("timeRegion: get end time" + formatEndTime + "休市")
            endTimeIdx += 1
            continue
        timeValue[1] = formatEndTime
        timeDict["1"] = formatEndTime
        break
    
    startTimeIdx = endTimeIdx + 1
    while(True):
        startTime = time.localtime(time.time() - startTimeIdx * 86400)
        formatStartTime= time.strftime("%Y-%m-%d", startTime)
        history = ts.get_h_data("000001", \
                                start = formatStartTime, \
                                end = formatStartTime, \
                                index = True)
        if (history is None or history.empty):
            print("timeRegion: get start time" + formatStartTime + "休市")
            startTimeIdx += 1
            continue
        timeValue[0] = formatStartTime
        timeIdx += 1
        timeDict[str(timeIdx + 1)] = formatStartTime
        startTimeIdx += 1
        if(timeIdx > regionNum):
            break
    print("timeDict")
    print(timeDict)

def statistics(day, tolerance, id):
    dayIdx = 0
    dayCalcIdx = 0
    dayCalcIdx1 = 1
    dayValue = [1, 2]
    belongto = stockBelongs(id)
    isWeNeed = False
    print("开始统计:" + id)
    if(belongto == "0"):
        return
    timeValue = ["", ""]
    timeDict = {}
    timeRegion(timeValue, day, timeDict)
    shHistory = ts.get_h_data("000001", \
                        start = timeValue[0], \
                        end = timeValue[1], \
                        index = True)
    shPercentChg = {}
    idx = 0
    print(shHistory)
    while(True):
        key = timeDict[str(idx + 1)]
        preKey = timeDict[str(idx + 2)]
        print(key)
        openValue = string.atof(shHistory.get_value(key, "close"))
        closeValue = string.atof(shHistory.get_value(preKey, "close"))
        value = (float(openValue) - float(closeValue)) / float(closeValue)
        print("shPercentChg")
        print(value)
        shPercentChg[key] = value
        idx += 1
        if(idx > day -1):
            break
    szHistory = ts.get_h_data("399001", \
                        start = timeValue[0], \
                        end = timeValue[1], \
                        index = True)
    cybHistory = ts.get_h_data("399006", \
                        start = timeValue[0], \
                        end = timeValue[1], \
                        index = True)
    stockHistory = ts.get_hist_data(id, \
                        start = timeValue[0], \
                        end = timeValue[1])
    print(stockHistory[0])
    while(dayIdx < day):
        belongToHistory = belongToHist(dayValue, dayCalcIdx, belongto)        
        
        dayValue[dayCalcIdx1] = dayValue[dayCalcIdx] + 1
        
        belongToHistory1 = belongToHist(dayValue, dayCalcIdx1, belongto)
        
        
        begin = belongToHistory1["close"]
        end = belongToHistory["close"]
        percentChg = (float(end) - float(begin)) / float(begin)       
        
        preTime = time.localtime(time.time() - dayValue[dayCalcIdx] * 86400)
        formatPreTime = time.strftime("%Y-%m-%d", preTime)
        stockHist = ts.get_hist_data(id, \
                                    start = formatPreTime,\
                                    end = formatPreTime)
        if (stockHist is None or stockHist.empty):
            print(id + formatPreTime + "停牌")
            dayIdx += 1
            dayValue[dayCalcIdx] = dayValue[dayCalcIdx1]
            dayValue[dayCalcIdx1] += 1
            continue
        
        compareStock = int( string.atof(stockHist.get_value(    \
                        formatPreTime, "p_change") * 100))
        compareBelongto = int(float(percentChg) * 10000)
        print("时间: " + formatPreTime + "个股涨跌:" + str(compareStock) \
                + "大盘涨跌:" + str(compareBelongto))
        isWeNeed = compareStock > compareBelongto
        if(not isWeNeed):
            break
            
        dayIdx += 1
        dayValue[dayCalcIdx] = dayValue[dayCalcIdx1]
        dayValue[dayCalcIdx1] += 1
    if (isWeNeed):
        file_result.write(id + " ")
        print(id+ "符合筛选条件")

file_obj = open("AllStock.txt")
try:
    all_text_lines = file_obj.readlines()
finally:
    file_obj.close()
    
file_stock_id = open("AllStockID.txt", "w+")
file_result = open("result.txt", "a+")
resultTime = time.localtime(time.time())
formatRestultTime = time.strftime("%Y-%m-%d %H:%M:%S", resultTime)
file_result.write("--------------------------------------\n")
file_result.write(formatRestultTime)
file_result.write("\n")
file_result.write("统计最近5日股票涨跌信息")
file_result.write("\n")

#print ts.get_h_data('399001', start = "2016-06-17", end = "2016-06-17", index=True)
#print ts.get_hist_data("600000")
    
for line in all_text_lines:
    sections = line.split(' ')
    file_stock_id.write(sections[1][1:7])
    file_stock_id.write("\n")
    statistics(5, 0, sections[1][1:7])

file_stock_id.close()
file_obj.close()
file_result.close()

#print ts.get_h_data("000001", start="2016-06-17", end="2016-06-18", index = True)
        
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

def belongToHist(dayCalcIdx, id):
    while(True):
        preTime = time.localtime(time.time() - dayCalcIdx * 86400)
        formatPreTime = time.strftime("%Y-%m-%d", preTime)
        print("获取:" + id + "在" + formatPreTime + "的数据")
        print("day" + str(dayCalcIdx))
        history = ts.get_h_data(id, \
                            start = formatPreTime, \
                            end = formatPreTime, \
                            pause=0.01, \
                            index = True)
        if (history is None):
            print("fuck")
            dayCalcIdx += 1
            continue 
        return history

def statistics(day, tolerance, id):
    dayIdx = 0
    dayCalcIdx = 1
    dayCalcIdx1 = 2
    belongto = stockBelongs(id)
    isWeNeed = False
    print("开始统计:" + id)
    if(belongto == "0"):
        return
    while(dayIdx < day):
        preTime = time.localtime(time.time() - (dayCalcIdx + 1) * 86400)
        formatPreTime = time.strftime("%Y-%m-%d", preTime)

        belongToHistory = belongToHist(dayCalcIdx, belongto)
        dayCalcIdx += 1
        print("get history 1: " + str(dayCalcIdx))
        belongToHistory1 = belongToHist(dayCalcIdx, belongto)
        
        begin = belongToHistory1["close"]
        end = belongToHistory["close"]
        percentChg = (float(end) - float(begin)) / float(begin)
        print("percentChg")
        print(percentChg)
        stockHist = ts.get_hist_data(id, \
                                    start = formatPreTime,\
                                    end = formatPreTime)
        print(stockHist["p_change"])
        compareStock = int( string.atof(stockHist["p_change"]) * 100)
        compareBelongto = int(float(percentChg) * 10000)
        print("时间: " + formatPreTime + "个股:" + compareStock \
                    + "   大盘:" + compareBelongto)
        isWeNeed = compareStock > compareBelongto
        if(not isWeNeed):
            break
            
        dayIdx += 1
        dayCalcIdx += 1
        dayCalcIdx += 1
    if (isWeNeed):
        file_result.write(id + " ")
        print("符合筛选条件")

file_obj = open("AllStock.txt")
try:
    all_text_lines = file_obj.readlines()
finally:
    file_obj.close()
    
file_stock_id = open("AllStockID.txt", "w+")
file_result = open("result.txt", "a+")
resultTime = time.localtime(time.time())
formatRestultTime = time.strftime("%Y-%m-%d %H:%M:%S", resultTime)
file_result.write(formatRestultTime);
file_result.write("\n");

#print ts.get_h_data('399001', start = "2016-06-17", end = "2016-06-17", index=True)
#print ts.get_hist_data("600000")
    
for line in all_text_lines:
    sections = line.split(' ')
    file_stock_id.write(sections[1][1:7])
    file_stock_id.write("\n")
    statistics(3, 0, sections[1][1:7])

file_stock_id.close()
file_obj.close()
file_result.close()

#print ts.get_h_data("000001", start="2016-06-17", end="2016-06-18", index = True)
        
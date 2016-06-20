# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tushare as ts

file_obj = open("AllStock.txt")
try:
    all_text_lines = file_obj.readlines()
finally:
    file_obj.close()
    
file_stock_id = open("AllStockID.txt", "w+")
    
for line in all_text_lines:
    sections = line.split(' ')
    file_stock_id.write(sections[1]);
    file_stock_id.write("\n")

file_stock_id.close()

#print ts.get_h_data("000001", start="2016-06-17", end="2016-06-18", index = True)

def logError(str):
    file_error = open("error.txt", "w+")
    file_error.write(str)
    file_error.write("\n")
    file_error.close()

def stockBelongs(id):
    if(id[0:1] == "60"):
        return "000001"
    elif(id[0:1] == "00"):
        return "399001"
    elif(id[0:1] == "30"):
        return "399006"
    else:
        logError("未知股票市场id：" + id)
        return "0"

def statistics(day, tolerance, id):
    dayIdx = 0
    belongto = stockBelongs(id)
    if(belongto == "0"):
        return
    while(dayIDx < day):
        
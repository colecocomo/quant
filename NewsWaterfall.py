# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 16:41:32 2016

@author: colec
"""

import tushare as ts
import time

file_result = open("NewsWaterfall.txt", "w+")

isLoop = True
while(isLoop):
    resultTime = time.localtime(time.time())
    formatResultTime = time.strftime("%Y-%m-%d %H:%M:%S", resultTime)
    file_result.write(formatResultTime)
    file_result.write("\n")
    newsList = ts.get_latest_news()
    if (newsList is None):
        continue
    print("test")
    
    for idx, dataRow in newsList.iterrows():
        file_result.write(str(idx))
        file_result.write("    ")
        file_result.write(dataRow["classify"].encode('utf-8'))
        file_result.write("    ")
        file_result.write(dataRow["title"].encode('utf-8'))
        file_result.write("    ")
        file_result.write(dataRow["time"])
        file_result.write("    ")
        file_result.write(dataRow["url"])
        file_result.write("\n")
    #time.sleep(5)
    isLoop = False
    
file_result.close()
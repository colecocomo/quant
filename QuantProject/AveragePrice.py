# -*- coding: utf-8 -*-
"""
Created on Mar 26 2018

@author: cole
"""

import tushare as ts
import time
import csv

current_ime = time.localtime(time.time() - 24*3600)
format_time = time.strftime("%Y-%m-%d", current_ime)

file_csv = open('./ClassifyHistory/AveragePrice' + format_time + '.csv', 'wb+')
spam_writer = csv.writer(file_csv, dialect='excel')
spam_writer.writerow(['code', 'name', 'average', "close", "growth"])

today_all = ts.get_today_all()
for index, row in today_all.iterrows():
    _code = row['code']
    _amount = row['amount']
    if _amount < 1:
        spam_writer.writerow([_code, row['name'].encode('gbk'), 0, 0, 0])
        continue
    print '\nget' + str(_code) + '\'s tick data'
    _tick_data = ts.get_tick_data(_code, date=format_time, pause=3)
    _total_volume = 0
    _total_amount = 0
    for _tick_index, _tick_row in _tick_data.iterrows():
        _total_volume += _tick_row['volume']
        _total_amount += _tick_row['price'] * _tick_row['volume']
    if _total_volume == 0:
        print '\ntotal volume is zero'
        continue
    _average_price = _total_amount / _total_volume
    spam_writer.writerow([_code, row['name'].encode('gbk'), "%.02f" % _average_price,
                          row['trade'], row['changepercent']])
    print '\n' + str(_code) + '\'s average price is: ' + "%.02f" % _average_price + ' close price is: ' + \
          str(row['trade']) + ' growth is: ' + str(row['changepercent'])
file_csv.close()

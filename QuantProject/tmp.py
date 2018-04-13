# -*- coding: utf-8 -*-
"""
Created on Mar 26 2018

@author: cole
"""


import csv
import time
import os

_day_idx = 0
g_statistics_day = 3
_day_count = 0
while _day_count < g_statistics_day:
    _current_ime = time.localtime(time.time() - _day_idx * 24 * 3600)
    _format_time = time.strftime("%Y-%m-%d", _current_ime)
    _day_idx += 1
    if not os.path.exists('./ClassifyHistory/AveragePrice' + _format_time + '.csv'):
        continue

    file_csv = open('./ClassifyHistory/AveragePrice' + _format_time + '.csv', 'rb')
    spam_reader = csv.reader(file_csv)

    file_csv_writer = open('./ClassifyHistory/AveragePrice' + _format_time + '_copy.csv', 'wb+')
    spam_writer = csv.writer(file_csv_writer, dialect='excel')
    spam_writer.writerow(['code', 'name', 'average', "close", 'open', 'high', 'low', "growth", 'average_growth'])

    _is_first_line = True
    for line in spam_reader:
        if _is_first_line:
            _is_first_line = False
            continue
        else:
            _code = line[0]
            _name = line[1]
            _average = line[2]
            _close = line[3]
            _open = line[4]
            _high = line[5]
            _low = line[6]
            _growth = line[7]
            _average_growth = '%.02f' % (float(line[8]) * 100)
            spam_writer.writerow([_code, _name, _average, _close,
                                  _open, _high, _low, _growth, _average_growth])
    file_csv.close()
    file_csv_writer.close()
    _day_count += 1


# -*- coding: utf-8 -*-
"""
Created on Apr. 9 11:15:39 2017

@author: cole
"""

import tushare as ts
import time
import csv
import os

_day_idx = 1
sh_index = '000001'
sz_index = '399001'
cy_index = '399006'

_basics_map = {}

_basics_csv = open('./ClassifyHistory/Classify2018-03-23.csv', 'rb')
_spam_basics_reader = csv.reader(_basics_csv)
_is_First_Line = True
for _line in _spam_basics_reader:
    if _is_First_Line:
        _is_First_Line = False
        continue
    else:
        _code = _line[0]
        _name = _line[1]
        _classify = _line[2]
        _basics_map[_code] = {'code': _code,
                              'name': _name,
                              'classify': _classify}

while True:
    current_ime = time.localtime(time.time() - _day_idx * 24 * 3600)
    format_time = time.strftime("%Y-%m-%d", current_ime)
    _day_idx += 1

    if os.path.exists('./ClassifyHistory/Classify' + format_time + '.csv'):
        continue
    print 'Mine date: ' + format_time
    _sh_k_data = ts.get_k_data(code=sh_index, start=format_time, end=format_time, index=True)
    if len(_sh_k_data.index) == 0:
        continue
    # _sz_k_data = ts.get_k_data(code=sz_index, start=format_time, end=format_time, index=True)
    # _cy_k_data = ts.get_k_data(code=cy_index, start=format_time, end=format_time, index=True)
    _classify_csv = open('./ClassifyHistory/Classify' + format_time + '.csv', 'wb+')
    _spam_classify_writer = csv.writer(_classify_csv, dialect='excel')
    _spam_classify_writer.writerow(['code', 'name', 'classify', "growth", "amount", "amount_percent"])

    _average_csv = open('./ClassifyHistory/AveragePrice' + format_time + '.csv', 'wb+')
    _spam_average_writer = csv.writer(_average_csv, dialect='excel')
    _spam_average_writer.writerow(['code', 'name', 'average', "close", 'open', 'high',
                                   'low', "growth", 'average_growth'])
    for _stock_candidate in _basics_map:
        _hist_data = ts.get_hist_data(code=_stock_candidate, start=format_time, end=format_time)
        _k_data = ts.get_k_data(code=_stock_candidate, start=format_time, end=format_time)
        print _k_data
        if len(_k_data.index) == 0 or len(_hist_data.index) == 0:
            _spam_classify_writer([_stock_candidate,
                                   _basics_map[_stock_candidate]['name'],
                                   _basics_map[_stock_candidate]['classify'],
                                   0, 0, 0])
            _spam_average_writer([_stock_candidate,
                                  _basics_map[_stock_candidate]['name'],
                                  0, 0, 0, 0, 0, 0, 0])
            continue
        else:
            _open = _k_data['open'].values[0]
            _close = _k_data['close'].values[0]
            _low = _k_data['low'].values[0]
            _high = _k_data['high'].values[0]
            _amount = float(_k_data['volume'].values[0]) * 10000
            _growth = _hist_data['p_change'].values[0]

            _spam_classify_writer([_stock_candidate,
                                   _basics_map[_stock_candidate]['name'],
                                   _basics_map[_stock_candidate]['classify'],
                                   _growth, 0, 0])





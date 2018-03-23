# -*- coding: utf-8 -*-
"""
Created on Mar. 22 11:15:39 2018

@author: cole
"""

import tushare as ts
import csv
import time
import os

g_statistics_day = 5
g_100_m = 100000000

_idx = 0
_day_idx = 0
_amount_dict = {}
while _idx < g_statistics_day:
    _current_ime = time.localtime(time.time() - _day_idx * 24 * 3600)
    _format_time = time.strftime("%Y-%m-%d", _current_ime)

    if os.path.exists('./ClassifyHistory/Classify' + _format_time + '.csv'):
        _idx += 1

        amount_csv = open('./ClassifyHistory/Classify' + _format_time + '.csv', 'rb')
        spam_amount_reader = csv.reader(amount_csv)
        is_first_line = True
        _format_time = _format_time.replace('-', '')
        for line in spam_amount_reader:
            if is_first_line:
                is_first_line = False
                continue
            else:
                _amount_percent = float(line[5])
                if _amount_percent < 0.00001:
                    continue
                _amount_str = line[4].decode('gbk').encode('utf-8')
                _amount = 0.0
                _code = int(line[0])
                if ' 亿' in _amount_str:
                    _amount_str = _amount_str.replace(' 亿', '')
                    _amount = float(_amount_str) * 100
                if ' 万' in _amount_str:
                    _amount_str = _amount_str.replace(' 万', '')
                    _amount = float(_amount_str) / 100
                if _code not in _amount_dict.keys():
                    _amount_dict[_code] = []
                _amount_dict[_code].append({'date': _format_time,
                                            'amount': _amount, 'amount_percent': _amount_percent})
        amount_csv.close()
    _day_idx += 1

amount_trend_csv = open('./ClassifyHistory/AmountTrend.csv', 'wb+')
amount_trend_csv.writelines(['code', 'date', 'amount', 'amount_percent\n'])
for _code in _amount_dict.keys():
    _list_idx = len(_amount_dict[_code]) - 1
    _amount_content_str = "%06d" % _code + ','
    while _list_idx >= 0:
        _amount_content = _amount_dict[_code][_list_idx]
        _amount_content_str += str(_amount_content['amount']) + ','
        if _list_idx != 0:
            _amount_content_str += ','
        else:
            _amount_content_str += '\n'
        _list_idx -= 1
    amount_trend_csv.writelines(_amount_content_str)
amount_trend_csv.close()

amount_percent_trend_csv = open('./ClassifyHistory/AmountPercentTrend.csv', 'wb+')
amount_percent_trend_csv.writelines(['code', 'date', 'amount', 'amount_percent\n'])
for _code in _amount_dict.keys():
    _list_idx = len(_amount_dict[_code]) - 1
    _amount_content_str = "%06d" % _code + ','
    while _list_idx >= 0:
        _amount_content = _amount_dict[_code][_list_idx]
        _amount_content_str += str(_amount_content['amount_percent']) + ','
        if _list_idx != 0:
            _amount_content_str += ','
        else:
            _amount_content_str += '\n'
        _list_idx -= 1
        amount_percent_trend_csv.writelines(_amount_content_str)
amount_percent_trend_csv.close()



# -*- coding: utf-8 -*-
"""
Created on Mar. 22 11:15:39 2018

@author: cole
"""

import csv
import time
import os

g_statistics_day = 3
g_amount_inc_percent = 1.6
g_100_m = 100000000

today_all_csv = open('./ClassifyHistory/today_all.csv', 'rb')
spam_today_all_reader = csv.reader(today_all_csv)
is_first_line_today_all = True
today_all_map = {}
for line in spam_today_all_reader:
    if is_first_line_today_all:
        is_first_line_today_all = False
        continue
    else:
        today_all_map[int(line[1])] = {'open': float(line[5]),
                                       'close': float(line[4]),
                                       'low': float(line[7]),
                                       'high': float(line[6])}

_idx = 0
_day_idx = 0
_amount_dict = {}
_candidate_count = 0
while _idx < g_statistics_day:
    _current_ime = time.localtime(time.time() - _day_idx * 24 * 3600)
    _format_time = time.strftime("%Y-%m-%d", _current_ime)

    if os.path.exists('./ClassifyHistory/Classify' + _format_time + '.csv'):
        _idx += 1

        amount_csv = open('./ClassifyHistory/Classify' + _format_time + '.csv', 'rb')
        spam_amount_reader = csv.reader(amount_csv)
        _is_first_line = True
        _format_time = _format_time.replace('-', '')
        for line in spam_amount_reader:
            if _is_first_line:
                _is_first_line = False
                continue
            else:
                _amount_percent = float(line[5])
                _growth = float(line[3])
                if _amount_percent < 0.00001:
                    continue
                _amount_str = line[4].decode('gbk').encode('utf-8')
                _amount = 0.0
                _code = int(line[0])
                if ' 亿' in _amount_str:
                    _amount_str = _amount_str.replace(' 亿', '')
                    _amount = float(_amount_str) * 100
                elif ' 万' in _amount_str:
                    _amount_str = _amount_str.replace(' 万', '')
                    _amount = float(_amount_str) / 100
                else:
                    _amount = float(_amount_str)
                if _code not in _amount_dict.keys():
                    _amount_dict[_code] = []
                _amount_dict[_code].append({'date': _format_time,
                                            'amount': _amount,
                                            'amount_percent': _amount_percent,
                                            'growth': _growth})
        amount_csv.close()
    _day_idx += 1

amount_trend_csv = open('./ClassifyHistory/AmountTrend.csv', 'wb+')
amount_trend_csv.writelines(['code', 'date', 'amount', 'amount_percent\n'])
for _code in _amount_dict.keys():
    _list_idx = len(_amount_dict[_code]) - 1
    _amount_content_str = "%06d" % _code + ','
    _amount_percent_str = ''
    while _list_idx >= 0:
        _amount_content = _amount_dict[_code][_list_idx]
        _amount_content_str += str(_amount_content['amount'])
        _amount_percent_str += str(_amount_content['amount_percent'])
        if _list_idx != 0:
            _amount_content_str += ','
            _amount_percent_str += ','
        else:
            _amount_content_str += ','
            _amount_percent_str += '\n'
        _list_idx -= 1
    amount_trend_csv.writelines(_amount_content_str + _amount_percent_str)
amount_trend_csv.close()

for _code in _amount_dict.keys():
    if len(_amount_dict[_code]) < g_statistics_day:
        continue
    _list_idx = len(_amount_dict[_code]) - 1
    _amount_content = _amount_dict[_code]
    _base = 0
    _base_percent = 0
    _growth = 0
    _amount_continue_inc = True
    _cur_price_emotion = True
    while _list_idx > 0:
        _amount_cur = _amount_content[_list_idx - 1]['amount']
        _amount_pre = _amount_content[_list_idx]['amount']
        if (_amount_pre * g_amount_inc_percent) >= _amount_cur:
            _amount_continue_inc = False
            break
        if _amount_content[_list_idx - 1]['growth'] <= 0:
            _amount_continue_inc = False
            break

        _list_idx -= 1
    if _amount_continue_inc:
        _open = today_all_map[_code]['open']
        _high = today_all_map[_code]['high']
        _low = today_all_map[_code]['low']
        _close = today_all_map[_code]['close']

        if _open > _close:
            _cur_price_emotion = False

        if (_high - _close) > (_close - _open) * 0.7:
            _cur_price_emotion = False
        
        if _amount_dict[_code][0]['growth'] >= 9.90:
            _cur_price_emotion = False

        if _cur_price_emotion:
            _candidate_count += 1
            print _code
print '\nCandidate count is: ' + str(_candidate_count)



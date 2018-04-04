# -*- coding: utf-8 -*-
"""
Created on Apr. 4 11:15:39 2018

@author: cole
"""

import csv
import time
import os
import tushare as ts

g_statistics_day = 9
g_amount_inc_percent = 1.5
g_100_m = 100000000


_idx = 0
_day_idx = 0
_amount_dict = {}
_candidate_count = 0
_fake_candidate_count = 0
while _idx < g_statistics_day:
    _current_ime = time.localtime(time.time() - _day_idx * 24 * 3600)
    _format_time = time.strftime("%Y-%m-%d", _current_ime)

    if os.path.exists('./ClassifyHistory/Classify' + _format_time + '.csv'):
        _idx += 1

        amount_csv = open('./ClassifyHistory/Classify' + _format_time + '.csv', 'rb')
        spam_amount_reader = csv.reader(amount_csv)
        _is_first_line = True
        # _format_time = _format_time.replace('-', '')
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

_left_sample_count = 2
_sample_idx = 0
_total_count = 0
for _code in _amount_dict.keys():
    if len(_amount_dict[_code]) < _left_sample_count:
        continue
    _sample_idx = len(_amount_dict[_code]) - 1
    while _sample_idx >= _left_sample_count:
        _total_count += 1
        _amount_continue_inc = True
        _cur_price_emotion = True
        _list_idx = _sample_idx
        _amount_content = _amount_dict[_code]
        _sample_1 = _amount_content[_list_idx]
        _sample_2 = _amount_content[_list_idx - 1]
        _sample_3 = _amount_content[_list_idx - 2]
        if (_sample_1['amount'] * g_amount_inc_percent) >= _sample_2['amount']:
            _amount_continue_inc = False
        if (_sample_2['amount'] * g_amount_inc_percent) >= _sample_3['amount']:
            _amount_continue_inc = False
        if _sample_2['growth'] <= 0:
            _amount_continue_inc = False
        if _sample_3['growth'] <= 0:
            _amount_continue_inc = False

        if _amount_continue_inc:
            _sample_k_data = ts.get_k_data(code='%06d' % _code, start=_sample_3['date'], end=_sample_3['date'])
            if len(_sample_k_data.index) == 1:
                _open = _sample_k_data.loc[_sample_k_data['date'] == _sample_3['date'], 'open'].values[0]
                _high = _sample_k_data.loc[_sample_k_data['date'] == _sample_3['date'], 'high'].values[0]
                _low = _sample_k_data.loc[_sample_k_data['date'] == _sample_3['date'], 'low'].values[0]
                _close = _sample_k_data.loc[_sample_k_data['date'] == _sample_3['date'], 'close'].values[0]

                if _open > _close:
                    _cur_price_emotion = False

                if (_high - _close) > (_close - _open) * 0.7:
                    _cur_price_emotion = False

                if _sample_3['growth'] >= 9.90:
                    _cur_price_emotion = False

        if _amount_continue_inc and _cur_price_emotion:
            _sample_next = _amount_content[_list_idx - 3]
            if _sample_next['growth'] > 0.0:
                _candidate_count += 1
            else:
                _fake_candidate_count += 1
        _sample_idx -= 1

print 'Candidate count is: ' + str(_candidate_count)
print 'Fake candidate count is: ' + str(_fake_candidate_count)
print 'Total count is: ' + str(_total_count)
print 'Accuracy rate is: %.02f' % \
      (float(_candidate_count) * 100 / (_candidate_count + _fake_candidate_count))

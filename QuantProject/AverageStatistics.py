# -*- coding: utf-8 -*-
"""
Created on Apr. 10 2018

@author: cole
"""

import os
import sys
import time
import csv
import matplotlib.pyplot as plt

g_statistics_day = 28

_idx = 0
_day_idx = 0
_amount_dict = {}
_average_dict = {}
while _idx < g_statistics_day:
    _current_ime = time.localtime(time.time() - _day_idx * 24 * 3600)
    _format_time = time.strftime("%Y-%m-%d", _current_ime)
    _format_time_key = int(time.strftime("%Y%m%d", _current_ime))

    if os.path.exists('./ClassifyHistory/AveragePrice' + _format_time + '.csv'):
        _idx += 1
        _average_csv = open('./ClassifyHistory/AveragePrice' + _format_time + '.csv', 'rb')
        _spam_average_reader = csv.reader(_average_csv)
        _is_first_average = True
        for _line in _spam_average_reader:
            if _is_first_average:
                _is_first_average = False
                continue
            else:
                _average_code = int(_line[0])
                _average_price = float(_line[2])
                _average_close = float(_line[3])
                _average_open = float(_line[4])
                _average_high = float(_line[5])
                _average_low = float(_line[6])
                _average_growth = float(_line[7])
                _average_average_growth = float(_line[8])
                if _average_code not in _average_dict.keys():
                    _average_dict[_average_code] = {}
                _average_dict[_average_code][_format_time_key] = {'date': _format_time,
                                                                  'average_price': _average_price,
                                                                  'close': _average_close,
                                                                  'open': _average_open,
                                                                  'high': _average_high,
                                                                  'low': _average_low,
                                                                  'growth': _average_growth,
                                                                  'average_growth': _average_average_growth}
        _average_csv.close()
    _day_idx += 1

for _code_candidate in _average_dict.keys():
    _candidate = _average_dict[_code_candidate]
    _time_list = _candidate.keys()
    _time_list.sort()
    _close_list = []
    _growth_list = []
    _average_list = []
    _average_growth_list = []
    _time_list_str = []
    _min_price = sys.float_info.max
    _max_price = 0
    _min_growth = sys.float_info.max
    _max_growth = 0
    for _time in _time_list:
        _time_list_str.append(str(_time))
    for _time in _time_list:
        _close_list.append(_candidate[_time]['close'])
        if _candidate[_time]['close'] < _min_price:
            _min_price = _candidate[_time]['close']
        if _candidate[_time]['close'] > _max_price:
            _max_price = _candidate[_time]['close']

        _growth_list.append(_candidate[_time]['growth'])
        if _candidate[_time]['growth'] < _min_growth:
            _min_growth = _candidate[_time]['growth']
        if _candidate[_time]['growth'] > _max_growth:
            _max_growth = _candidate[_time]['growth']

        _average_list.append(_candidate[_time]['average_price'])
        if _candidate[_time]['average_price'] < _min_price:
            _min_price = _candidate[_time]['average_price']
        if _candidate[_time]['average_price'] > _max_price:
            _max_price = _candidate[_time]['average_price']

        _average_growth_list.append(_candidate[_time]['average_growth'])
        if _candidate[_time]['average_growth'] < _min_growth:
            _min_growth = _candidate[_time]['average_growth']
        if _candidate[_time]['average_growth'] > _max_growth:
            _max_growth = _candidate[_time]['average_growth']

    plt.figure(figsize=(14, 7), dpi=80)
    plt.title(_code_candidate)
    plt.grid(True)

    _ax_1 = plt.subplot(111)
    _ax_1.plot(_time_list_str, _close_list, color="b",
               linewidth=2.0, linestyle="-", label="close")
    _ax_1.plot(_time_list_str, _average_list, color="g",
               linewidth=2.0, linestyle="-", label="average")
    _ax_1.legend(loc="upper left", shadow=True)
    _ax_1.set_ylabel("price")
    _ax_1.set_ylim(_min_price * 0.95, _max_price * 1.05)

    _ax_2 = _ax_1.twinx()
    _ax_2.plot(_time_list_str, _growth_list, color="r",
               linewidth=2.0, linestyle="--", label="growth")
    _ax_2.plot(_time_list_str, _average_growth_list, color="c",
               linewidth=2.0, linestyle="--", label="average_growth")
    _ax_2.legend(loc="upper right", shadow=True)

    _ax_2.set_ylabel("growth")
    if _min_growth < 0:
        _ax_2.set_ylim(_min_growth * 1.2, _max_growth * 1.2)
    else:
        _ax_2.set_ylim(_min_growth * 0.8, _max_growth * 1.2)

    _ax_1.set_xlabel("Date")
    for label in _ax_1.get_xticklabels():
        label.set_color("red")
        label.set_rotation(45)
    plt.show()
    # os.system('pause')




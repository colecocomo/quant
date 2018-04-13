# -*- coding: utf-8 -*-
"""
Created on Apr. 4 11:15:39 2018

@author: cole
"""

import csv
import time
import os
import matplotlib.pyplot as plt

g_statistics_day = 28
g_amount_inc_percent = 1.5
g_100_m = 100000000


_idx = 0
_day_idx = 1
_amount_dict = {}
_average_dict = {}
_candidate_count = 0
_candidate_growth = 0
_fake_candidate_count = 0.0
_fake_candidate_growth = 0.0
_init_asset = 140000.0
_alpha = _init_asset
_alpha_daily = _init_asset
_alpha_dict = {}
_trade_fee = 0.0025
while _idx < g_statistics_day:
    _current_ime = time.localtime(time.time() - _day_idx * 24 * 3600)
    _format_time = time.strftime("%Y-%m-%d", _current_ime)

    if os.path.exists('./ClassifyHistory/AveragePrice' + _format_time + '.csv'):
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
                _average_dict[_average_code][_format_time] = {'average_price': _average_price,
                                                              'close': _average_close,
                                                              'open': _average_open,
                                                              'high': _average_high,
                                                              'low': _average_low,
                                                              'growth': _average_growth,
                                                              'average_growth': _average_average_growth}

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

_left_sample_count = 3
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
            if _sample_3['date'] in _average_dict[_code].keys():
                _average_sample = _average_dict[_code][_sample_3['date']]
                _open = _average_sample['open']
                _high = _average_sample['high']
                _low = _average_sample['low']
                _close = _average_sample['close']

                if _open > _close:
                    _cur_price_emotion = False

                if (_high - _close) > (_close - _open) * 0.7:
                    _cur_price_emotion = False

                if _sample_3['growth'] >= 9.90:
                    _cur_price_emotion = False

        if _amount_continue_inc and _cur_price_emotion:
            _sample_next = _amount_content[_list_idx - 3]
            _sample_sell = _amount_content[_list_idx - 4]
            _buy_price = 0
            _sell_price = 0
            if _sample_next['date'] in _average_dict[_code].keys():
                _buy_price = _average_dict[_code][_sample_next['date']]['open']
            if _sample_sell['date'] in _average_dict[_code].keys():
                _sell_price = _average_dict[_code][_sample_sell['date']]['open']
            if _sample_next['growth'] > 0.0:
                _candidate_count += 1
                _candidate_growth += _sample_next['growth']
            else:
                _fake_candidate_count += 1
                _fake_candidate_growth += _sample_next['growth']
            if _buy_price != 0 and _sell_price != 0:
                _alpha *= (1 + ((_sell_price - _buy_price) / _buy_price))
                _alpha_date = int(_sample_next['date'].replace('-', ''))
                if _alpha_date not in _alpha_dict.keys():
                    _alpha_dict[_alpha_date] = []
                _alpha_dict[_alpha_date].append({'code': _code,
                                                 'date': _sample_next['date'],
                                                 'growth': '%.02f' % ((_sell_price - _buy_price) / _buy_price),
                                                 'buy': _buy_price,
                                                 'sell': _sell_price})
        _sample_idx -= 1

print 'Candidate count is: ' + str(_candidate_count) + \
      ' average growth is: %.02f' % (_candidate_growth / _candidate_count)
print 'Fake candidate count is: ' + str(_fake_candidate_count) + \
      ' average growth is: %.02f' % (_fake_candidate_growth / _fake_candidate_growth)
print 'Total count is: ' + str(_total_count)
print 'Accuracy rate is: %.02f' % \
      (float(_candidate_count) * 100 / (_candidate_count + _fake_candidate_count))
# print 'Alpha is: ' + '%.02f' % _alpha
_alpha_dict_keys_sorted = _alpha_dict.keys()
_alpha_dict_keys_sorted.sort()
_plot_time = []
_plot_profit = []
for _sorted_date in _alpha_dict_keys_sorted:
    _plot_time.append(str(_sorted_date))
    _daily_candidate = _alpha_dict[_sorted_date]
    _daily_candidate_count = len(_daily_candidate)

    _profit_tmp = 0
    for _sorted_candidate_sample in _daily_candidate:
        # print _sorted_candidate_sample
        _print_tmp = (1 - _trade_fee) * (_alpha_daily / _daily_candidate_count) * \
                       (1 + ((_sorted_candidate_sample['sell'] -
                              _sorted_candidate_sample['buy']) / _sorted_candidate_sample['buy']))
        _profit_tmp += (1 - _trade_fee) * (_alpha_daily / _daily_candidate_count) * \
                       (1 + ((_sorted_candidate_sample['sell'] -
                              _sorted_candidate_sample['buy']) / _sorted_candidate_sample['buy']))
        # print str(_sorted_candidate_sample['code']) + ('profit is: %.02f' % _print_tmp)
    print str(_sorted_date) + (' profit is: %.02f' % (_profit_tmp - _alpha_daily))
    _alpha_daily = _profit_tmp
    _plot_profit.append(_alpha_daily)
print 'Alpha day count is: ' + str(len(_alpha_dict.keys()))
print 'Alpha daily is: ' + '%.02f' % (_alpha_daily - _init_asset) + \
      ' growth is: %.02f' % ((_alpha_daily - _init_asset) / _init_asset)

plt.figure(figsize=(14, 7), dpi=80)
plt.title('Amount Statistics')
plt.grid(True)

_ax_1 = plt.subplot(111)
_ax_1.plot(_plot_time, _plot_profit, color="b",
           linewidth=2.0, linestyle="-", label="profit")
_ax_1.legend(loc="upper left", shadow=True)
_ax_1.set_ylabel("profit")

_ax_1.set_xlabel("Date")
for label in _ax_1.get_xticklabels():
    label.set_color("red")
    label.set_rotation(45)
plt.show()



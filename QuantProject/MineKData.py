# -*- coding: utf-8 -*-
"""
Created on Apr. 9 11:15:39 2018

@author: cole
"""

import csv
import time
import os

sh_index = '000001'
sz_index = '399001'
cy_index = '399006'

_basics_csv = open('./ClassifyHistory/Classify2018-03-26.csv', 'rb')
_spam_basics_reader = csv.reader(_basics_csv)
_is_first_line = True
_basics_map = {}
for _line in _spam_basics_reader:
    if _is_first_line:
        _is_first_line = False
        continue
    else:
        _code = _line[0]
        _name = _line[1]
        _classify = _line[2]
        _basics_map[_code] = {'code': _code,
                              'name': _name,
                              'classify': _classify}

_sh_csv = open('./StockData/KDataQfq/SH' + sh_index + '.csv', 'rb')
_spam_sh_reader = csv.reader(_sh_csv)
_sh_amount_map = {}
for _sh_line in _spam_sh_reader:
    if len(_sh_line) == 0:
        break
    _date = _sh_line[0]
    _open = _sh_line[1]
    _high = _sh_line[2]
    _low = _sh_line[3]
    _close = _sh_line[4]
    _amount = _sh_line[6]
    _sh_amount_map[_date] = {'date': _date,
                             'open': _open,
                             'high': _high,
                             'low': _low,
                             'close': _close,
                             'amount': _amount}
_sh_csv.close()

_sz_csv = open('./StockData/KDataQfq/SZ' + sz_index + '.csv', 'rb')
_spam_sz_reader = csv.reader(_sz_csv)
_sz_amount_map = {}
for _sz_line in _spam_sz_reader:
    if len(_sz_line) == 0:
        break
    _date = _sz_line[0]
    _open = _sz_line[1]
    _high = _sz_line[2]
    _low = _sz_line[3]
    _close = _sz_line[4]
    _amount = _sz_line[6]
    _sz_amount_map[_date] = {'date': _date,
                             'open': _open,
                             'high': _high,
                             'low': _low,
                             'close': _close,
                             'amount': _amount}
_sz_csv.close()

_cy_csv = open('./StockData/KDataQfq/SZ' + cy_index + '.csv', 'rb')
_spam_cy_reader = csv.reader(_cy_csv)
_cy_amount_map = {}
for _cy_line in _spam_cy_reader:
    if len(_cy_line) == 0:
        break
    _date = _cy_line[0]
    _open = _cy_line[1]
    _high = _cy_line[2]
    _low = _cy_line[3]
    _close = _cy_line[4]
    _amount = _cy_line[6]
    _cy_amount_map[_date] = {'date': _date,
                             'open': _open,
                             'high': _high,
                             'low': _low,
                             'close': _close,
                             'amount': _amount}
_cy_csv.close()


_day_idx = 1
_mine_count = 0
_max_mine_count = 30
while True:
    _current_ime = time.localtime(time.time() - _day_idx * 24 * 3600)
    _format_time = time.strftime("%Y-%m-%d", _current_ime)
    _format_time_ym = time.strftime("%Y%m", _current_ime)
    _format_time_average = _format_time.replace('-', '')
    _day_idx += 1

    if os.path.exists('./ClassifyHistory/Classify' + _format_time + '.csv'):
        print 'Existing ' + './ClassifyHistory/Classify' + _format_time + '.csv'
        continue

    if _mine_count > _max_mine_count:
        break

    if _format_time not in _sh_amount_map.keys():
        continue

    print 'Mine ' + _format_time
    print 'Mining ' + str(_mine_count) + '/' + str(_max_mine_count)

    _mine_count += 1

    _k_data_csv = open('./ClassifyHistory/Classify' + _format_time + '.csv', 'wb+')
    _spam_k_data_writer = csv.writer(_k_data_csv, dialect='excel')
    _spam_k_data_writer.writerow(['code', 'name', 'classify', "growth", "amount", "amount_percent"])

    _average_csv = open('./ClassifyHistory/AveragePrice' + _format_time + '.csv', 'wb+')
    _spam_average_writer = csv.writer(_average_csv, dialect='excel')
    _spam_average_writer.writerow(['code', 'name', 'average',
                                   "close", 'open', 'high', 'low', "growth", 'average_growth'])

    _code_count = 1
    for _code in _basics_map.keys():
        print 'Mining progress ' + str(_code_count) + '/' + str(len(_basics_map.keys()))
        _code_count += 1
        high_bit = int(int(_code) / 100000)
        _csv_file_name = ''
        _csv_file_name_average = ''
        _amount_basics = 0
        if high_bit == 6:
            _csv_file_name = './StockData/KDataQfq/SH' + _code + '.csv'
            _csv_file_name_average = './StockData/TickData/' + _format_time_ym + 'SH/' + \
                                     _format_time_average + '/' + _code + '_' + \
                                     _format_time_average + '.csv'
            _amount_basics = _sh_amount_map[_format_time]['amount']
        elif high_bit == 3:
            _csv_file_name = './StockData/KDataQfq/SZ' + _code + '.csv'
            _amount_basics = _cy_amount_map[_format_time]['amount']
            _csv_file_name_average = './StockData/TickData/' + _format_time_ym + 'SZ/' + \
                                     _format_time_average + '/' + _code + '_' + \
                                     _format_time_average + '.csv'
        else:
            _csv_file_name = './StockData/KDataQfq/SZ' + _code + '.csv'
            _amount_basics = _sz_amount_map[_format_time]['amount']
            _csv_file_name_average = './StockData/TickData/' + _format_time_ym + 'SZ/' + \
                                     _format_time_average + '/' + _code + '_' + \
                                     _format_time_average + '.csv'
        if not os.path.exists(_csv_file_name):
            continue
        _k_data_input = open(_csv_file_name, 'rb')
        _spam_k_data_input_reader = csv.reader(_k_data_input)
        _input_growth = 0
        _amount_percent = 0
        _input_open = '0'
        _input_high = '0'
        _input_low = '0'
        _input_close = '0'
        for _input_line in _spam_k_data_input_reader:
            if len(_input_line) == 0:
                break
            _input_date = _input_line[0]
            if _input_date != _format_time:
                _pre_close = _input_line[4]
            else:
                if float(_pre_close) > 0.0001:
                    _input_growth = (float(_input_line[4]) - float(_pre_close)) / float(_pre_close)
                if float(_amount_basics) > 0.0001:
                    _amount_percent = float(_input_line[6]) / float(_amount_basics)
                _input_open = _input_line[1]
                _input_high = _input_line[2]
                _input_low = _input_line[3]
                _input_close = _input_line[4]
                _spam_k_data_writer.writerow([_code,
                                              _basics_map[_code]['name'],
                                              _basics_map[_code]['classify'],
                                              '%.02f' % (_input_growth * 100),
                                              _input_line[6],
                                              '%.02f' % (_amount_percent * 100)])

        if not os.path.exists(_csv_file_name_average):
            _spam_average_writer.writerow([_code,
                                           _basics_map[_code]['name'],
                                           0,
                                           0,
                                           0,
                                           0,
                                           0,
                                           0,
                                           0])
        else:
            _average_input_csv = open(_csv_file_name_average, 'rb')
            _spam_average_input_reader = csv.reader(_average_input_csv)
            _is_first_average_line = True
            _total_volume = 0
            _total_amount = 0
            _average_growth = 0
            for _average_line in _spam_average_input_reader:
                if len(_average_line) == 0:
                    break
                if _is_first_average_line:
                    _is_first_average_line = False
                    continue
                else:
                    _total_volume += int(_average_line[3])
                    _total_amount += float(_average_line[5])
            if _total_volume == 0:
                print '\ntotal volume is zero'
                continue
            else:
                _average_price = _total_amount / (_total_volume * 100)
                if float(_input_close) < 0.0001:
                    _average_growth = 0
                else:
                    _average_growth = (_average_price - float(_input_close)) / float(_input_close)
                _spam_average_writer.writerow([_code,
                                               _basics_map[_code]['name'],
                                               "%.02f" % _average_price,
                                               _input_close,
                                               _input_open,
                                               _input_high,
                                               _input_low,
                                               '%.02f' % (_input_growth * 100),
                                               '%.02f' % (_average_growth * 100)])
        _k_data_input.close()
        _average_input_csv.close()

    _k_data_csv.close()
    _average_csv.close()

print 'Mine finish.'


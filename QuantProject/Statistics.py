# -*- coding: utf-8 -*-
"""
Created on Mar. 6 11:15:39 2017

@author: cole
"""

import tushare as ts
import time
import csv
import os

sh_index = '000001'
sz_index = '399001'
cy_index = '399006'
_100_m = 100000000

current_ime = time.localtime(time.time() - 0)
format_time = time.strftime("%Y-%m-%d", current_ime)
format_time_asset = format_time.replace('-', '')


file_csv = open('./ClassifyHistory/Classify' + format_time + '.csv', 'wb+')
spam_writer = csv.writer(file_csv, dialect='excel')
spam_writer.writerow(['code', 'name', 'classify', "growth", "amount", "amount_percent"])

is_exist = os.path.exists('./ClassifyHistory/AssetFow' + sh_index + '.csv')
asset_flow_csv_sh = open('./ClassifyHistory/AssetFow' + sh_index + '.csv', 'ab+')
spam_asset_writer_sh = csv.writer(asset_flow_csv_sh, dialect='excel')
if not is_exist:
    spam_asset_writer_sh.writerow(['date', 'code', 'amount', 'growth'])

is_exist = os.path.exists('./ClassifyHistory/AssetFow' + sz_index + '.csv')
asset_flow_csv_sz = open('./ClassifyHistory/AssetFow' + sz_index + '.csv', 'ab+')
spam_asset_writer_sz = csv.writer(asset_flow_csv_sz, dialect='excel')
if not is_exist:
    spam_asset_writer_sz.writerow(['date', 'code', 'amount', 'growth'])

is_exist = os.path.exists('./ClassifyHistory/AssetFow' + cy_index + '.csv')
asset_flow_csv_cy = open('./ClassifyHistory/AssetFow' + cy_index + '.csv', 'ab+')
spam_asset_writer_cy = csv.writer(asset_flow_csv_cy, dialect='excel')
if not is_exist:
    spam_asset_writer_cy.writerow(['date', 'code', 'amount', 'growth'])

index_all = ts.get_index()
sh_amount = index_all.loc[index_all['code'] == sh_index, 'amount'].values[0]
sh_growth = index_all.loc[index_all['code'] == sh_index, 'change'].values[0]
cy_amount = index_all.loc[index_all['code'] == cy_index, 'amount'].values[0]
cy_growth = index_all.loc[index_all['code'] == cy_index, 'change'].values[0]
sz_amount = index_all.loc[index_all['code'] == sz_index, 'amount'].values[0]
sz_growth = index_all.loc[index_all['code'] == sz_index, 'change'].values[0]

spam_asset_writer_sh.writerow([format_time_asset, sh_index, sh_amount, sh_growth])
spam_asset_writer_sz.writerow([format_time_asset, sz_index, sz_amount, sz_growth])
spam_asset_writer_cy.writerow([format_time_asset, cy_index, cy_amount, cy_growth])

asset_flow_csv_sh.close()
asset_flow_csv_cy.close()
asset_flow_csv_sz.close()

today_all = ts.get_today_all()
today_all.to_csv(path_or_buf='./ClassifyHistory/today_all.csv', encoding='gbk')
classify = ts.get_industry_classified()
classify.to_csv(path_or_buf='./ClassifyHistory/classify.csv', encoding='gbk')
for index, classifyRow in classify.iterrows():
    code = classifyRow['code']
    if len(today_all.loc[today_all['code'] == code]) != 1:
        continue
    stock_name = classifyRow["name"].encode("gbk")
    classify_name = classifyRow["c_name"].encode("gbk")
    growth = today_all.loc[today_all['code'] == code, 'changepercent'].values[0]
    amount = today_all.loc[today_all['code'] == code, "amount"].values[0]
    high_bit = int(int(code) / 100000)
    amount_percent = .0
    if high_bit == 6:
        print 'code is:' + code + str(amount)
        amount_percent = amount * 100 / (sh_amount * _100_m)
        print amount_percent
    elif high_bit == 3:
        amount_percent = amount * 100 / (cy_amount * _100_m)
    else:
        amount_percent = amount * 100 / (sz_amount * _100_m)
    amount_string = ''
    if amount >= _100_m:
        amount_string = "%.02f" % (amount / _100_m) + " 亿"
    else:
        amount_string = "%.02f" % (amount / 10000) + " 万"
    spam_writer.writerow([code, stock_name,
                          classify_name, growth, amount_string.decode('utf-8').encode('gbk'),
                          "%.03f" % (amount_percent)])

    # print code + classifyRow["c_name"] + str(growth) + "%.02f" % (amount_percent)
file_csv.close()
print "statistics end"

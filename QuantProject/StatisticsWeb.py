# -*- coding: utf-8 -*-
"""
Created on Mar. 7 11:15:39 2018

@author: cole
"""

from flask import Flask, jsonify
import csv

sh_index = '000001'
sz_index = '399001'
cy_index = '399006'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello stranger'

@app.route('/assetflow')
def asset_flow():
    asset_flow_csv_sh = open('./ClassifyHistory/AssetFow' + sh_index + '.csv', 'rb')
    spam_asset_reader_sh = csv.reader(asset_flow_csv_sh)
    is_first_line = True
    asset_flow_dict_sh = {}
    for line in spam_asset_reader_sh:
        if is_first_line:
            is_first_line = False
            continue
        else:
            asset_flow_dict_sh[line[0]] = {'amount': float(line[2]), 'growth': float(line[3])}
    asset_flow_csv_sh.close()

    asset_flow_csv_sz = open('./ClassifyHistory/AssetFow' + sz_index + '.csv', 'rb')
    spam_asset_reader_sz = csv.reader(asset_flow_csv_sz)
    is_first_line = True
    asset_flow_dict_sz = {}
    for line in spam_asset_reader_sz:
        if is_first_line:
            is_first_line = False
            continue
        else:
            asset_flow_dict_sz[line[0]] = {'amount': float(line[2]), 'growth': float(line[3])}
    asset_flow_csv_sz.close()

    asset_flow_csv_cy = open('./ClassifyHistory/AssetFow' + cy_index + '.csv', 'rb')
    spam_asset_reader_cy = csv.reader(asset_flow_csv_cy)
    is_first_line = True
    asset_flow_dict_cy = {}
    for line in spam_asset_reader_cy:
        if is_first_line:
            is_first_line = False
            continue
        else:
            asset_flow_dict_cy[line[0]] = {'amount': float(line[2]), 'growth': float(line[3])}
    asset_flow_csv_cy.close()

    return jsonify(sh=asset_flow_csv_sh,
                   sz=asset_flow_csv_sz,
                   cy=asset_flow_csv_cy)


if __name__ == '__main__':
    app.run()

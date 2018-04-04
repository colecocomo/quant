# -*- coding: utf-8 -*-
"""
Created on Mar. 12 11:15:39 2018

@author: cole
"""

import tushare as ts
from wxpy import *

bot = Bot(console_qr=True, cache_path=True)

inst_detail = ts.inst_detail()
inst_detail.to_csv(path_or_buf='./ClassifyHistory/inst_detail.csv', encoding='gbk')

inst_tops = ts.inst_tops()
inst_tops.to_csv(path_or_buf='./ClassifyHistory/inst_tops.csv', encoding='gbk')


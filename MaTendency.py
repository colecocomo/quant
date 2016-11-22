# -*- coding: utf-8 -*-

import csv

file_csv = open('MaTendency.csv', 'wb+')
spamwriter = csv.writer(file_csv,dialect='excel')
spamwriter.writerow(['stock', 'maDiffPercent5', 'maDiffPercent10', 'maDiffPercent20', "dayCnt", "curStatus", "maxVolumePercentRecently"])

csvSourceFile = file('ma_tiki.csv', 'rb')
reader = csv.reader(csvSourceFile)

for line in reader:
    ma5 = (float)(line[1])
    ma10 = (float)(line[2])
    ma20 = (float)(line[3])

    if ma20< 0:
        continue
    if ma10>0:
        continue
    if ma5>0:
        continue

    stock = line[0]
    tmp1 = line[4]
    tmp2 = line[5]
    tmp3 = line[6]

    spamwriter.writerow([stock, ma5, ma10, ma20, tmp1, tmp2, tmp3])

csvSourceFile.close()
file_csv.close()


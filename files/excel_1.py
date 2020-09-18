# -*- coding:utf-8 -*-
import xdrlib, sys
import xlrd
import xlwt
import time,datetime
import DateTime

rexcel = xlrd.open_workbook('E:\pythondoc\hbp.xls')
wexcel = xlwt.Workbook()
sheet2 = wexcel.add_sheet('sheet22', cell_overwrite_ok = True)
sheet1 = rexcel.sheets()[0]
rows = sheet1.nrows
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
sheet2.write(0, 0, str('入院日期'))

for i in range(1, rows):
    t = sheet1.cell_value(i, 3)
    time.strptime(t, "%Y.%m.%d")
    sheet2.write(i, 0, t)
#    print(v)
wexcel.save('E:\pythondoc\hbp2.xls')


while False:
    if  t in sheet2():
        break
    else:
        break



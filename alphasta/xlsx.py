import xlwt  # 写入文件
import xlrd  # 打开excel文件

xls = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = xls.add_sheet('sheet1')

fr = open("D:\\xaa.txt", 'r',encoding='UTF-8')
lines = fr.readlines()
row = 1
for line in lines:
    str_line = str(line)
    ls_line = list(str_line)
    # print(ls_line)
    # print(type(ls_line))
    # print(len(ls_line))
    col = -1
    for ele in ls_line:
        col += 1
        if ele ==' ':
            col -= 1
        else:
            sheet.write(row,col,ele)
    row += 1

xls.save('test.xls')
fr.close()
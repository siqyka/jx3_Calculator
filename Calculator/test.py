import xlwings as xw
# myExcel = openpyxl.load_workbook('Calculator.xlsm',keep_vba=True,data_only=True) #获取表格文件

# sheet1 = myExcel['正常']
# cell1 = sheet1['U27'].value
# print(cell1)

# myExcel = openpyxl.load_workbook('Calculator.xlsm',keep_vba=True,data_only=False)
# sheet2 = myExcel['配装页面']
# sheet2['O35']=8
# myExcel.save('Calculator.xlsm')

# myExcel = openpyxl.load_workbook('Calculator.xlsm',keep_vba=True,data_only=True) #获取表格文件
# sheet1 = myExcel['正常']
# cell1 = sheet1['U27'].value
# print(cell1)


import xlwings as xw
app=xw.App(visible=False,add_book=False)
wb = app.books.open('Calculator.xlsm')
sheet = wb.sheets['正常']
print(sheet.range('U27').value )
sheet1 = wb.sheets['配装页面']
sheet1.range('W12').value='计算增益'
sheet1.range('W13').value='凌雪阵'
print(sheet.range('U27').value )
wb.save()
wb.close()
app.quit()
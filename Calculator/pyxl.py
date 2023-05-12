import xlrd
import xlwt

data = xlrd.open_workbook("cpypy.xlsx")
print(data.sheets())
# from PyQt5.QtWidgets import *
# import sys
# from PyQt5 import QtCore
# class Main(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("主窗口")
#         button = QPushButton("弹出子窗", self)
#         button.clicked.connect(self.show_child)
#         self.child_window = Child()
 
#     def show_child(self):
#         self.child_window.my_Signal.connect(self.active_exit)
#         self.child_window.show()
        
#     def active_exit(self):
#         print(111111)
        
# class Child(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("我是子窗口啊")
        
#     my_Signal = QtCore.pyqtSignal(str)
    
#     def sendEditContent(self):
#         content = '1'
#         self.my_Signal.emit(content)

#     def closeEvent(self, event):
#         print(2222222)
#         # self.sendEditContent()

 
# # 运行主窗口
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
 
#     window = Main()
#     window.show()
 
#     sys.exit(app.exec_())







# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QFileDialog, QWidget
# import json,xlwt
# class MyWindow(QWidget):
#     def __init__(self):
#         super(MyWindow, self).__init__()
#         self.myButton = QtWidgets.QPushButton(self)
#         self.myButton.setObjectName("btn")
#         self.myButton.setText("按钮")
#         self.myButton.clicked.connect(self.save_xls)
#         self.txt='hellow'
#         self.jso = ['hellow']
#         self.xls = 'hellow'
 
 
#     def save_txt(self):
#         txt=self.txt
#         filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "/" ,'txt(*.txt)')#前面是地址，后面是文件类型,得到输入地址的文件名和地址txt(*.txt*.xls);;image(*.png)不同类别
#         file=open(filepath,'w')
#         print(filepath)
#         file.write(txt)
#     def save_json(self):
#         jso=self.jso
#         filepath,type = QFileDialog.getSaveFileName(self,'文件保存','/','json(*.json)')
#         print(filepath)
#         with open(filepath,'w') as file_obj:
#             json.dump(jso,file_obj)
#     def save_xls(self):
#         xls=self.xls
#         book = xlwt.Workbook(encoding='utf-8', style_compression=0)
#         sheet = book.add_sheet('number', cell_overwrite_ok=True)
#         sheet.write(0, 0, xls)
#         filepath, type = QFileDialog.getSaveFileName(self, '文件保存', '/', 'xls(*.xls)')
#         print(filepath)
#         book.save(filepath)
 
 
 
 
 
 
# if __name__ == "__main__":
#     import sys
 
#     app = QtWidgets.QApplication(sys.argv)
#     myshow = MyWindow()
#     myshow.show()
#     sys.exit(app.exec_())










#coding:utf-8
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

class MainUi(QtWidgets.QMainWindow):

    # 界面初始化
    def __init__(self, parent=None):
        # 导入文件按钮
        self.button_load_file = QtWidgets.QPushButton('选择文件', self.main_widget)
        # 绑定事件
        self.button_load_file.clicked.connect(self.button_load_file_clicked)

        # 创建QSettings，配置文件是tmp/.temp
        self.setting = QSettings('tmp/.temp', QSettings.IniFormat) 
        
        # 设置UTF8编码，反正保存配置文件时出现乱码
        self.setting.setIniCodec('UTF-8') 
        
        # 读取上一次的目录路径
        self.last_path = self.setting.value('LastFilePath')
        
        # 如果字符串为空，将路径索引到根目录
        if self.last_path is None:
            self.last_path = '/' # 根盘符

    # 点击打开文件
    def button_load_file_clicked(self):
        # 设置过滤器
        format_str = ' '.join(['*.pdf']) 
        
        # 弹出打开文件的对话窗
        fname, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "select pdf", self.last_path, "PDF files (%s)" % (format_str,))
        
        # 如果文件为空，取消后续指令
        if fname is None or len(fname) <= 0:
            return
            
        try:
            #将多个文件转为列表
            self.file_path_list = [fname_item for fname_item in fname] 
            
            # 保存当前目录的路径到配置文件中，另外如果不存在'tmp/.temp'文件该函数会自动创建
            self.setting.setValue('LastFilePath', os.path.dirname(self.file_path_list[0]))
            
             # 将路径设为''程序会使用上一次的路径
            self.last_path = ''
            
        except Exception as e:
            # 发生异常，弹窗警告 
            msg = QtWidgets.QMessageBox.warning(self, "Warning", "PDF打开失败%s" % e, buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)

MainUi()
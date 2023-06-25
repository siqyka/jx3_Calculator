from PyQt5.QtCore import QSettings
from PyQt5 import QtCore, QtWidgets, QtGui
import os
from functools import partial
from PyQt5.QtWidgets import *
import json

class MenuC():
    openf_Signal=QtCore.pyqtSignal(str)
    def __init__(self,M) -> None:
        self.M=M
        self.setting = QSettings('../userData/.temp', QSettings.IniFormat) 
        self.setting.setIniCodec('UTF-8') 
        self.last_path = self.setting.value('LastFilePath')
        if self.last_path is None:
            self.last_path = '/' # 根盘符
            
    def openJx3cFile(self):
        # 设置过滤器
        format_str = ' '.join(['*.jx3c']) 
        # 弹出打开文件的对话窗
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self.M, "打开", self.last_path, "jx3c files (%s)" % (format_str,))

        # 如果文件为空，取消后续指令
        if not fname:
            return

        try:
            self.setting.setValue('LastFilePath', os.path.dirname(fname))
            self.setting.setValue('LastOpenFilePath', fname)
             # 将路径设为''程序会使用上一次的路径
            self.last_path = ''
            return self.readJx3cFile(fname),fname
        except Exception as e:
            # 发生异常，弹窗警告 
            msg = QtWidgets.QMessageBox.warning(self, "Warning", "打开失败%s" % e, buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
            
    def readJx3cFile(self,path):
        with open(path, 'r',encoding='utf-8') as f:
            return json.dumps(f.read())
        
    
    def saveJx3cFile(self):
        pass
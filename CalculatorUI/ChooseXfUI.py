from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtCore,QtWidgets
from functools import partial
import tools
import Configure

xfs={
    '傲血战意':701,
    '花间游':703,
    '太虚剑意':703,
    '紫霞功':703,
    '冰心诀':702,
    '易筋经':703,
    '问水诀':703,
    '天罗诡道':703,
    '惊羽诀':703,
    '毒经':703,
    '焚影圣诀':703,
    '笑尘诀':703,
    '分山劲':703,
    '莫问':703,
    '北傲诀':703,
    '凌海诀':703,
    '隐龙诀':703,
    '太玄经':703,
    '无方':703,
    '孤锋诀':703,
}

class ChooseXF(QWidget):
    my_Signal = QtCore.pyqtSignal(str)
    def __init__(self):
        # self.MainWindow = QtWidgets.QMainWindow()
        super().__init__()
        self.setWindowTitle("心法选择")
        self.resize(500,400)
        self.setWindowFlags(  QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.ToolTip |QtCore.Qt.WindowCloseButtonHint )
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.obj=Configure.GameConf().pro
        self.zfui()
    
    def zfui(self):
        # self.btn = QPushButton('打开新窗口',self)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 0, 460, 400))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        # xfs=[x for x in range(1,21)]
        # _translate = QtCore.QCoreApplication.translate
        x,y=0,0
        for k,v in xfs.items():
            if y>3:
                y=0
                x+=1
            self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
            self.pushButton.setObjectName(str(v))
            self.gridLayout.addWidget(self.pushButton, x, y, 1, 1)
            self.pushButton.setText(k)
            self.pushButton.clicked.connect(partial(self.sendEditContent,self.pushButton.objectName()))
            y+=1
        # QtCore.QMetaObject.connectSlotsByName(self)
        
    def sendEditContent(self,obj):
        self.obj=obj
        tools.Conf().writeConf('professional','pro',obj)
        # self.__init__(MainWindow)
        # self.closeEvent
        self.close()

    def closeEvent(self, event):
        # self.my_Signal.emit(self.obj)
        if self.obj not in ['701','702']:
            self.my_Signal.emit('701')
        else:
            self.my_Signal.emit(self.obj)
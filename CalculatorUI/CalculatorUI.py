import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (QApplication, QWidget, QGroupBox, QMenu, QAction,
#                              QPushButton, QCheckBox, QRadioButton,
#                              QVBoxLayout, QGridLayout,QCompleter)
from functools import partial
import tools
import Configure
from ExtendedTools import ExtendedComboBox
import requests
import Cevent
import time


class CalculatorUI(QtWidgets.QWidget,QtCore.QObject):
    def __init__(self, MainWindow):
        self.PRO=Configure.GameConf().getPro()
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1660, 1200)
        self.MainWindow.setFixedSize(self.MainWindow.width(), self.MainWindow.height())
        self.MainWindow.setWindowIcon(QtGui.QIcon(
            Configure.MainWindowConf.windowIcon))
        self.MainWindow.setWindowTitle(Configure.MainWindowConf.windowTitle)
        self.Calculators = QtWidgets.QWidget(self.MainWindow)
        self.Calculators.setObjectName("Calculators")
        self._translate = QtCore.QCoreApplication.translate
        self.position=None
        self.userData=None
        self.materielPanelUI()
        self.materielSelectionUI()
        self.combatOptionsUI()
        self.propertyBenefitsUI()
        self.qiXueUI()
        self.rareBookUI()
        self.buffBoxUI()
        self.menubarUI()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def menubarUI(self):
        self.MainWindow.setCentralWidget(self.Calculators)
        self.menubar = QtWidgets.QMenuBar(
            self.MainWindow, objectName='menubar')
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1800, 26))
        self.menubar.setStyleSheet('#menubar{font-size:15px;}')
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)
        # '文件'菜单
        self.fileMenu = QtWidgets.QMenu(self.menubar, objectName='fileMenu')
        self.fnew = QtWidgets.QAction(self.MainWindow, objectName='fnew')
        self.fsave = QtWidgets.QAction(self.MainWindow, objectName='fsave')
        self.osave = QtWidgets.QAction(self.MainWindow, objectName='osave')
        self.dimport = QtWidgets.QAction(self.MainWindow, objectName='dimport')
        self.jx3box = QtWidgets.QAction(self.MainWindow, objectName='jx3box')
        self.importMenu = QtWidgets.QMenu(
            self.fileMenu, objectName='importMenu')
        self.importMenu.addAction(self.jx3box)
        # '帮助'菜单
        self.helps = QtWidgets.QMenu(self.menubar, objectName='importMenu')
        self.helps.setObjectName("helps")
        self.useHelp = QtWidgets.QAction(self.MainWindow, objectName='useHelp')
        self.lxfs = QtWidgets.QAction(self.MainWindow, objectName='lxfs')
        self.project = QtWidgets.QAction(self.MainWindow, objectName='project')
        self.about = QtWidgets.QAction(self.MainWindow, objectName='about')

        self.fileMenu.addAction(self.fnew)
        self.fileMenu.addAction(self.fsave)
        self.fileMenu.addAction(self.osave)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importMenu.menuAction())
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.dimport)
        self.helps.addAction(self.useHelp)
        self.helps.addSeparator()
        self.helps.addAction(self.lxfs)
        self.helps.addSeparator()
        self.helps.addAction(self.project)
        self.helps.addAction(self.about)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.helps.menuAction())

        _translate = QtCore.QCoreApplication.translate
        self.fileMenu.setTitle(_translate("MainWindow", "文件"))
        self.importMenu.setTitle(_translate("MainWindow", "导入"))
        self.helps.setTitle(_translate("MainWindow", "帮助"))
        self.fnew.setText(_translate("MainWindow", "新建"))
        self.fsave.setText(_translate("MainWindow", "保存"))
        self.osave.setText(_translate("MainWindow", "另存为"))
        self.dimport.setText(_translate("MainWindow", "导出"))
        self.jx3box.setText(_translate("MainWindow", "从jx3box导入"))
        self.useHelp.setText(_translate("MainWindow", "使用帮助"))
        self.lxfs.setText(_translate("MainWindow", "联系作者"))
        self.project.setText(_translate("MainWindow", "项目主页"))
        self.about.setText(_translate("MainWindow", "关于项目"))

    def materielPanelUI(self):
        # 装备属性面板
        self.materielPanel = QtWidgets.QGroupBox(self.Calculators)
        self.materielPanel.setGeometry(QtCore.QRect(10, 10, 600, 680))
        # self.materielPanel.setAutoFillBackground(False)
        # self.materielPanel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.materielPanel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.materielPanel.setObjectName("materielPanel")

        # 装备格子坐标
        materielPlaids = [(10, 20), (10, 151), (10, 292), (10, 433), (10, 574)] +\
            [(495, 20), (495, 110), (495, 202), (495, 296),
             (495, 391), (495, 485), (495, 580)]

        # 循环创建装备格子
        for n, m in enumerate(materielPlaids, 1):
            # 设置装备格子底，选中格子显示边框颜色，提示
            self.mpQLabel = QtWidgets.QLabel(
                self.materielPanel, objectName="mpQLabel_{}".format(str(n).zfill(2)))
            x, y = m
            self.mpQLabel.setGeometry(QtCore.QRect(x-2, y-2, 89, 89))
            # self.mpQLabel.setStyleSheet('#mpQLabel_'+str(n).zfill(2)+'{background-color: transparent;}')
            self.mpQLabel.setProperty("name", "mpQLabel")
            # 装备格子
            self.mpPushButton = QtWidgets.QPushButton(
                self.materielPanel, objectName="materielPlaids_{}".format(str(n).zfill(2)))
            self.mpPushButton.setGeometry(QtCore.QRect(*m, 85, 85))
            self.mpPushButton.setStyleSheet('#materielPlaids_'+str(n).zfill(
                2)+'{border-image:url(../artResources/defaultLattice/'+str(n).zfill(2)+'.png);}')
            self.mpPushButton.setProperty("name", "mpPushButton")
            self.mpPushButton.clicked.connect(
                partial(self.materielPlaidEvent, self.mpPushButton))

        # 属性面板
        self.attributeFrame = QtWidgets.QFrame(
            self.materielPanel, objectName='attributeFrame')
        self.attributeFrame.setGeometry(QtCore.QRect(130, 30, 320, 650))
        self.mpHorizontalLayoutWidget = QtWidgets.QWidget(
            self.attributeFrame, objectName='mpHorizontalLayoutWidget')
        self.mpHorizontalLayoutWidget.setGeometry(
            QtCore.QRect(20, 30, 281, 471))
        self.mpHorizontalLayout = QtWidgets.QHBoxLayout(
            self.mpHorizontalLayoutWidget, objectName='mpHorizontalLayout')
        self.mpHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_l = QtWidgets.QVBoxLayout(
            objectName='verticalLayout_l')
        self.verticalLayout_r = QtWidgets.QVBoxLayout(
            objectName='verticalLayout_r')
        self.mpHorizontalLayout.addLayout(self.verticalLayout_l)
        self.mpHorizontalLayout.addLayout(self.verticalLayout_r)

        # 默认显示
        for afi, afm in enumerate(Configure.GameConf().getAttributeName(), 1):
            self.afLabell = QtWidgets.QLabel(
                self.mpHorizontalLayoutWidget, objectName="afLabell_{}".format(str(afi).zfill(2)))
            self.afLabell.setText(afm)
            self.afLabell.setAlignment(Qt.AlignCenter)
            self.afLabell.setProperty("name", "afLabel")
            self.afLabelr = QtWidgets.QLabel(
                self.mpHorizontalLayoutWidget, objectName="afLabelr_{}".format(str(afi).zfill(2)))
            self.afLabelr.setText('578883')
            self.afLabelr.setAlignment(Qt.AlignCenter)
            self.afLabelr.setProperty("name", "afLabel")
            self.verticalLayout_l.addWidget(self.afLabell)
            self.verticalLayout_r.addWidget(self.afLabelr)

        # dps显示栏
        self.dpsLabel = QtWidgets.QLabel(
            self.attributeFrame, objectName='dpsLabel')
        self.dpsLabel.setGeometry(QtCore.QRect(10, 530, 300, 110))
        self.dpsLabel.setText('9999999')
        self.dpsLabel.setAlignment(Qt.AlignCenter)
        # self.dpsLabel.setStyleSheet("QLabel{color:red;font-size:50px;}")
        self.dpsLabel.setProperty("name", "dpsLabel")

    # def setComboDate(self,obj):
        
    # 点击装备格子事件
    def materielPlaidEvent(self, mobj):
        # 选择改变底色
        for i in range(1, 13):
            lableobjname = 'mpQLabel_'+str(i).zfill(2)
            lableobj = self.materielPanel.findChild(
                QtWidgets.QLabel, lableobjname)
            lableobj.setStyleSheet(
                '#'+lableobjname+'{background-color: transparent;}')
        lableobjname = 'mpQLabel_'+mobj.objectName()[-2:]
        self.position=mobj.objectName()[-2:]
        lableobj = self.materielPanel.findChild(QtWidgets.QLabel, lableobjname)
        lableobj.setStyleSheet(
            '#'+lableobjname+'{background-color: rgb(41,121,255);}')
        
        # 获取装备选择区域数据
        # m=Cevent.Cevents().getMateriel(lableobjname[-2:])
        pds,pxs=Cevent.Cevents().getFM(lableobjname[-2:])
        cobj=self.materielSelection.findChild(QtWidgets.QComboBox, 'msComboBox')
        dfm=self.materielSelection.findChild(QtWidgets.QComboBox, 'dfm')
        xfm=self.materielSelection.findChild(QtWidgets.QComboBox, 'xfm')
        dfm.clear()
        xfm.clear()
        # 大附魔
        dfm.addItem('请选择',-1)
        for ind,x in enumerate(pds,1):
            dfm.addItem(x["Name"],{"id": x['ID']})
            # dfm.setItemData(ind, {"id": x['ID']})
            
        # 小附魔
        xfm.addItem('请选择',-1)
        for ind,x in enumerate(pxs,1):
            xfm.addItem(x["Name"],{"id": x['ID']})
            # xfm.setItemData(ind, {"id": x['ID']})

        self.materielItemsEvent()

        if self.userData:
            xfmid=91315
            data = {"id": xfmid}
            i=xfm.findData(data) 
            d={"id": 91315,'icon':'17945'}
            ii=cobj.findData(d) 
            cobj.setCurrentIndex(ii)
            print(ii)
        # 装备名称组装
        # for ind,x in enumerate(m,1):
        #     cobj.addItem('{} ({}品  {})'.format(x['Name'],x['Level'],x['MagicType']))
        #     cobj.setItemData(ind, {"id": x['ID'],'icon':x['_IconID']})
        

        # 第一次随便搞，保存了读取配装文件
        # if xxx:
            # 通过装备id查找序号
            # pzindex=cobj.findData({"id": 34401})
        
        # 打开界面就应该读取保存的装备
        # pzindex=0
        # cobj.setCurrentIndex(pzindex)
        # data = cobj.itemData(cobj.currentIndex())
        # print(data)
        # if data:
        #     tm=Cevent.Cevents().getAMaterielHtml(data['id'],lableobjname[-2:])
        #     self.attributeDisplay.setText(self._translate("self", tm))
            
        #     x=Cevent.Cevents().getAMateriel(data['id'],lableobjname[-2:])
        #     self.starHidden(x["MaxStrengthLevel"])

     
    # 装备选择UI
    def materielSelectionUI(self):
        self.materielSelection = QtWidgets.QFrame(
            self.Calculators, objectName='materielSelection')
        self.materielSelection.setGeometry(QtCore.QRect(630, 10, 600, 680))
        # self.materielSelection.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.materielSelection.setFrameShadow(QtWidgets.QFrame.Raised)

        self.attributeSelection = QtWidgets.QGroupBox(
            self.materielSelection, objectName='attributeSelection')
        self.attributeSelection.setGeometry(QtCore.QRect(10, 10, 580, 50))

        self.msHorizontalLayoutWidget = QtWidgets.QWidget(
            self.attributeSelection, objectName='msHorizontalLayoutWidget')
        self.msHorizontalLayoutWidget.setGeometry(QtCore.QRect(5, 5, 570, 40))
        self.msHorizontalLayout = QtWidgets.QHBoxLayout(
            self.msHorizontalLayoutWidget, objectName='msHorizontalLayout')
        self.msHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        # 属性筛选
        attributeSelectionL = ["会心", "会效", "破防", "破招", "无双",  "加速"]
        for asi, asm in enumerate(attributeSelectionL, 1):
            self.asCheckBox = QtWidgets.QCheckBox(
                self.msHorizontalLayoutWidget, objectName="asCheckBox_{}".format(str(asi).zfill(2)))
            self.msHorizontalLayout.addWidget(self.asCheckBox)
            self.asCheckBox.setProperty("name", "asCheckBox")
            self.asCheckBox.setText(asm)
            self.asCheckBox.stateChanged.connect(
                    partial(self.materielItemsEvent))

        self.gradeSelection = QtWidgets.QGroupBox(
            self.materielSelection, objectName='gradeSelection')
        self.gradeSelection.setGeometry(QtCore.QRect(10, 70, 580, 50))
        self.LGradeLineEdit = QtWidgets.QLineEdit(
            self.gradeSelection, objectName='LGradeLineEdit')
        self.LGradeLineEdit.textChanged.connect(
                    partial(self.materielItemsEvent))
        self.LGradeLineEdit.setGeometry(QtCore.QRect(10, 10, 80, 30))
        self.HGradeLineEdit = QtWidgets.QLineEdit(
            self.gradeSelection, objectName='HGradeLineEdit')
        self.HGradeLineEdit.setGeometry(QtCore.QRect(140, 10, 80, 30))
        self.HGradeLineEdit.textChanged.connect(
                    partial(self.materielItemsEvent))
        # 设置只能输入数字
        self.LGradeLineEdit.setValidator(QtGui.QIntValidator())
        self.HGradeLineEdit.setValidator(QtGui.QIntValidator())
        
        self.PZ = QtWidgets.QLabel(self.gradeSelection, objectName='PZ')
        self.PZ.setGeometry(QtCore.QRect(95, 10, 40, 30))
        self.PZ.setText('品至')
        self.P = QtWidgets.QLabel(self.gradeSelection, objectName='P')
        self.P.setGeometry(QtCore.QRect(225, 10, 20, 30))
        self.P.setText('品')
        
        # self.gsHorizontalSlider = QtWidgets.QSlider(
        #     self.gradeSelection, objectName='gsHorizontalSlider')
        # self.gsHorizontalSlider.setGeometry(QtCore.QRect(260, 10, 300, 30))
        # self.gsHorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        
        # 双滑动条的问题有待解决
        # self.gsHorizontalSlider_1 = QtWidgets.QSlider(self.gradeSelection,objectName='gsHorizontalSlider')
        # self.gsHorizontalSlider_1.setGeometry(QtCore.QRect(260, 10, 300, 30))
        # self.gsHorizontalSlider_1.setOrientation(QtCore.Qt.Horizontal)
        self.materielSelectionBox = QtWidgets.QGroupBox(
            self.materielSelection, objectName='materielSelectionBox')
        self.materielSelectionBox.setGeometry(QtCore.QRect(10, 130, 580, 50))

        # 装备选择框
        self.msComboBox = ExtendedComboBox(
            self.materielSelectionBox)
        # self.msComboBox = QtWidgets.QComboBox(
        #     self.materielSelectionBox)
        self.msComboBox.setObjectName('msComboBox')
        self.msComboBox.setGeometry(QtCore.QRect(10, 10, 560, 30))
        # self.msComboBox.addItems(['火龙沥泉', '碎魂', '赤乌流火', '赤乌'])
        # self.msComboBox.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.msComboBox.setEditable(True)
        # self.msComboBox.setCompleter(QCompleter(['火龙沥泉', '碎魂', '赤乌流火','赤乌']))

        self.msComboBox.currentIndexChanged.connect(
            partial(self.materielMsComboBoxChangeEvent, self.msComboBox))
        self.msComboBox.setStyleSheet('#msComboBox{font-size:20px;}')

        # 装备属性展示
        self.attributeDisplay = QtWidgets.QLabel(
            self.materielSelection, objectName='attributeDisplay')
        self.attributeDisplay.setGeometry(QtCore.QRect(10, 200, 270, 470))
        self.attributeDisplay.setFixedWidth(250)
        self.attributeDisplay.setWordWrap(True)
        # 判读是否有配装保存，没有啥都不用显示
        # self.attributeDisplay.setText(self._translate("self", "<html><head/><body>\
        #     <p align=\"center\"><span style=\" font:15px  Microsoft YaHei; \
        #     color:#00aeff;\"> pirate ship  </span>\
        # </p></body></html>"))
        
        
        # 清除精炼按钮
        self.xpushButton = QtWidgets.QPushButton(
            self.materielSelection, objectName='xpushButton')
        self.xpushButton.setGeometry(QtCore.QRect(390, 208, 30, 30))
        # self.xpushButton.setStyleSheet('#xpushButton{border-image:url(../artResources/defaultLattice/x.png);}')
        self.xpushButton.setStyleSheet("#xpushButton{border-image: url(../artResources/defaultLattice/x.png)}"
                                       "#xpushButton:hover{border-image: url(../artResources/defaultLattice/x_r.png)}")
        self.xpushButton.clicked.connect(
                partial(self.refiningButtonEvent,0))

        labText = ['精炼等级', '小附魔', '五行石镶嵌', '大附魔', '五彩石镶嵌']
        labxy = [(300, 210, 300, 20), (300, 300, 300, 20), (300, 370, 300, 20),
                 (300, 440, 300, 20), (300, 510, 300, 20)]
        for i in range(5):
            self.refiningLabel = QtWidgets.QLabel(
                self.materielSelection, objectName='refiningLabel')
            self.refiningLabel.setGeometry(QtCore.QRect(*labxy[i]))
            self.refiningLabel.setStyleSheet('#refiningLabel{font-size:20px;}')
            self.refiningLabel.setText(labText[i])

        cbText = [('xfm', (300, 330, 280, 30)), ('wxs1', (300, 400, 90, 30)), ('wxs2', (393, 400, 90, 30)),
                  ('wxs3', (487, 400, 90, 30)), ('dfm',
                                                 (300, 470, 280, 30)), ('wcs1', (300, 540, 280, 30)),
                  ('wcs2', (300, 570, 280, 30)), ('wcs3', (300, 600, 280, 30)), ('wcs4', (300, 630, 280, 30))]
        for cb in range(9):
            self.cbComboBox = ExtendedComboBox(self.materielSelection)
            self.cbComboBox.setObjectName(cbText[cb][0])
            self.cbComboBox.setGeometry(QtCore.QRect(*cbText[cb][1]))

        wxs1=self.materielSelection.findChild(
                QtWidgets.QComboBox, 'wxs1')
        wxs2=self.materielSelection.findChild(
                QtWidgets.QComboBox, 'wxs2')
        wxs3=self.materielSelection.findChild(
                QtWidgets.QComboBox, 'wxs3')
        wcs1=self.materielSelection.findChild(
                QtWidgets.QComboBox, 'wcs1')
        wcs2=self.materielSelection.findChild(
                QtWidgets.QComboBox, 'wcs2')
        wcs3=self.materielSelection.findChild(
                QtWidgets.QComboBox, 'wcs3')
        wcs4=self.materielSelection.findChild(
                QtWidgets.QComboBox, 'wcs4')
        # 测试数据
        wcs2.addItems(['会心', '会效', '破防'])
        wcs3.addItems(['会心', '会效', '破防'])
        wcs4.addItems(['会心', '会效', '破防'])
        wcs1.addItems(['肆', '伍', '陆'])
        wxs1.addItems(["0","1","2","3","4","5","6","7","8"])
        wxs2.addItems(["0","1","2","3","4","5","6","7","8"])
        wxs3.addItems(["0","1","2","3","4","5","6","7","8"])
        for n in range(1, 9):
            # 精炼等级
            ry = 250
            rx = 300+((n-1)*35)
            self.refiningButton = QtWidgets.QPushButton(
                self.materielSelection, objectName="refiningButton_{}".format(str(n).zfill(2)))
            self.refiningButton.setGeometry(QtCore.QRect(rx, ry, 30, 30))
            self.refiningButton.setStyleSheet('#refiningButton_'+str(n).zfill(
                2)+'{border-image:url(../artResources/defaultLattice/5j_no.png);}')
            self.refiningButton.setProperty("name", "refiningButton")
            self.refiningButton.clicked.connect(
                partial(self.refiningButtonEvent, self.refiningButton))

    def materielItemsEvent(self):
        needMagic=[]
        for g in self.msHorizontalLayoutWidget.findChildren(QtWidgets.QCheckBox):
            if g.isChecked():
                needMagic.append(g.text())
        minLevel=0
        maxLevel=9999999
        
        
        if  self.LGradeLineEdit.text()!='':
            minLevel=int(self.LGradeLineEdit.text())
        if  self.HGradeLineEdit.text()!='':
            maxLevel=int(self.HGradeLineEdit.text())
        print(minLevel,maxLevel)
        if self.position:
            m=Cevent.Cevents().getMateriel(self.position,minLevel=minLevel,maxLevel=maxLevel,needMagic=needMagic)
            cobj=self.materielSelection.findChild(QtWidgets.QComboBox, 'msComboBox')
            cobj.clear()
            cobj.addItem('请选择')
                
            for ind,x in enumerate(m,1):
                cobj.addItem('{} ({}品  {})'.format(x['Name'],x['Level'],x['MagicType']),{"id": x['ID'],'icon':x['_IconID']})
                # cobj.setItemData(ind, {"id": x['ID'],'icon':x['_IconID']})
        else:
            pass
        
    # 依据可精炼等级显示星星
    def starHidden(self,x):
        for i in range(8, int(x), -1):
            lableobj = self.materielSelection.findChild(
                QtWidgets.QPushButton, 'refiningButton_{}'.format(str(i).zfill(2)))
            lableobj.setHidden(True)
        # 显示等级
        for ii in range(1, int(x)+1):
            lableobj = self.materielSelection.findChild(
                QtWidgets.QPushButton, 'refiningButton_{}'.format(str(ii).zfill(2)))
            lableobj.setHidden(False)
            
    # 装备选择后事件
    def materielMsComboBoxChangeEvent(self, msComboBox):
        mstext = msComboBox.currentText()
        data = msComboBox.itemData(msComboBox.currentIndex())
        # print(data)
        if  data and self.position:
            x=Cevent.Cevents().getAMateriel(data['id'],self.position)
            self.starHidden(x["MaxStrengthLevel"])
            
            tm=Cevent.Cevents().getAMaterielHtml(data['id'],self.position)
            self.attributeDisplay.setText(self._translate("self", tm))
            
            
            mpp=self.materielPanel.findChild(
                QtWidgets.QPushButton, 'materielPlaids_{}'.format(self.position))
            # 图片展示数据，数据全则去除if else
            if data['icon'] in ['17815','19357']:
                mpp.setStyleSheet('#materielPlaids_'+self.position+'{border-image:url(../artResources/materielImg/'+str(data['icon']+'.png);}'))
            else:
                mpp.setStyleSheet('#materielPlaids_'+self.position+'{border-image:url(../artResources/materielImg/mo.png);}')
        # self.starHidden(x)
        else:
            pass
        
    # 装备精炼事件
    def refiningButtonEvent(self, robj):
        if robj==0:
            starIndex=0
        else:
            starIndex = int(robj.objectName()[-2:])
        # 选择等级后变实心
        for i in range(1, starIndex+1):
            lableobjname = 'refiningButton_{}'.format(str(i).zfill(2))
            lableobj = self.materielSelection.findChild(
                QtWidgets.QPushButton, lableobjname)
            lableobj.setStyleSheet(
                '#'+lableobjname+'{border-image:url(../artResources/defaultLattice/5j_yes.png);}')
        # 把高于等级的变空心
        for ii in range(8, starIndex, -1):
            lableobjname = 'refiningButton_{}'.format(str(ii).zfill(2))
            lableobj = self.materielSelection.findChild(
                QtWidgets.QPushButton, lableobjname)
            lableobj.setStyleSheet(
                '#'+lableobjname+'{border-image:url(../artResources/defaultLattice/5j_no.png);}')

    # 战斗选项ui
    def combatOptionsUI(self):
        self.combatOptions = QtWidgets.QFrame(
            self.Calculators, objectName='combatOptions')
        self.combatOptions.setGeometry(QtCore.QRect(1250, 10, 400, 310))
        self.combatOptions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.combatOptions.setFrameShadow(QtWidgets.QFrame.Raised)
        self.coHorizontalLayoutWidget = QtWidgets.QWidget(
            self.combatOptions, objectName='coHorizontalLayoutWidget')
        self.coHorizontalLayoutWidget.setGeometry(
            QtCore.QRect(2, 30, 396, 278))
        self.coHorizontalLayout = QtWidgets.QHBoxLayout(
            self.coHorizontalLayoutWidget, objectName='coHorizontalLayout')
        self.coHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.coVerticalLayoutL = QtWidgets.QVBoxLayout(
            objectName='coVerticalLayoutL')
        self.coVerticalLayoutR = QtWidgets.QVBoxLayout(
            objectName='coVerticalLayoutR')
        # 选项名称
        combatOptionsL=Configure.GameConf().getCombatOptions()
        for coi, com in enumerate(combatOptionsL, 1):
            self.coLabel = QtWidgets.QLabel(
                self.coHorizontalLayoutWidget, objectName="coLabel_{}".format(str(coi).zfill(2)))
            self.coVerticalLayoutL.addWidget(self.coLabel)
            self.coLabel.setAlignment(Qt.AlignCenter)
            self.coLabel.setText(com)
        # 选项选择
        for coii, _ in enumerate(combatOptionsL, 1):
            self.coComboBox = QtWidgets.QComboBox(
                self.coHorizontalLayoutWidget, objectName="coComboBox_{}".format(str(coii).zfill(2)))
            self.coVerticalLayoutR.addWidget(self.coComboBox)

        self.coHorizontalLayout.addLayout(self.coVerticalLayoutL)
        self.coHorizontalLayout.addLayout(self.coVerticalLayoutR)
        # 标题
        self.coTitleFrame = QtWidgets.QFrame(self.combatOptions)
        self.coTitleFrame.setGeometry(QtCore.QRect(0, 0, 400, 28))
        self.coTitleLabel = QtWidgets.QLabel(
            self.coTitleFrame, objectName='coTitleLabel')
        self.coTitleLabel.setGeometry(QtCore.QRect(0, 0, 400, 28))
        self.coTitleLabel.setAlignment(Qt.AlignCenter)
        self.coTitleLabel.setText('战斗选项')

    # 属性收益ui
    def propertyBenefitsUI(self):
        self.propertyBenefits = QtWidgets.QFrame(
            self.Calculators, objectName='propertyBenefits')
        self.propertyBenefits.setGeometry(QtCore.QRect(1250, 350, 400, 340))
        # self.propertyBenefits.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.propertyBenefits.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pbTitleFrame = QtWidgets.QFrame(self.propertyBenefits)
        self.pbTitleFrame.setGeometry(QtCore.QRect(0, 0, 400, 28))
        self.pbTitleLabel = QtWidgets.QLabel(
            self.pbTitleFrame, objectName='pbTitleLabel')
        self.pbTitleLabel.setGeometry(QtCore.QRect(0, 0, 400, 28))
        self.pbTitleLabel.setAlignment(Qt.AlignCenter)
        self.pbTitleLabel.setText('属性收益')
        self.pbLabel = QtWidgets.QLabel(
            self.propertyBenefits, objectName='pbLabel')
        self.pbLabel.setGeometry(QtCore.QRect(3, 30, 398, 310))
        self.pbLabel.setStyleSheet(
            '#pbLabel{border-image:url(../artResources/defaultLattice/sy.png);}')

    # 奇穴UI
    def qiXueUI(self):
        self.qiXueFrame = QtWidgets.QFrame(
            self.Calculators, objectName='qiXueFrame')
        self.qiXueFrame.setGeometry(QtCore.QRect(10, 710, 600, 231))
        self.qiXueFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.qiXueFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.qxTitleFrame = QtWidgets.QFrame(self.qiXueFrame)
        self.qxTitleFrame.setGeometry(QtCore.QRect(0, 0, 600, 28))
        self.qxTitleLabel = QtWidgets.QLabel(
            self.qxTitleFrame, objectName='qxTitleLabel')
        self.qxTitleLabel.setGeometry(QtCore.QRect(0, 0, 600, 28))
        self.qxTitleLabel.setAlignment(Qt.AlignCenter)
        self.qxTitleLabel.setText('奇穴')

        qiXuexy = [(10, 40, 88, 80), (107, 40, 88, 80), (206, 40, 88, 80), (305, 40, 88, 80),
                   (404, 40, 88, 80), (503, 40, 88, 80), (10,
                                                          130, 88, 80), (107, 130, 88, 80),
                   (206, 130, 88, 80), (305, 130, 88, 80), (404, 130, 88, 80), (503, 130, 88, 80)]
        all=Configure.GameConf().getQixue()
        for qxi, qxm in enumerate(qiXuexy, 1):
            self.qxComboBox = QtWidgets.QComboBox(
                self.qiXueFrame, objectName="qxComboBox_{}".format(str(qxi).zfill(2)))
            self.qxComboBox.setGeometry(QtCore.QRect(*qxm))
            self.qxComboBox.activated.connect(partial(self.qiXueEvent,self.qxComboBox))

            size = QtCore.QSize(75, 75) 
            self.qxComboBox.setIconSize(size)

            theQx=all[str(qxi)]
            # 需要修改为多进程加快加载速度
            ind=0
            _translate = QtCore.QCoreApplication.translate
            for k,v in theQx.items():
            #     # 从jx3box获取
            #     url = "https://icon.jx3box.com/icon/{}.png".format(str(v['icon']))
            #     print(url)
            #     icon = QtGui.QIcon()
            #     try:
            #         response = requests.get(url)
            #         pixmap = QtGui.QPixmap()
            #         pixmap.loadFromData(response.content)
            #         icon = QtGui.QIcon(pixmap)
            #     except:
            #         pass
            #     self.qxComboBox.addItem(icon,'\n'.join(v['name']))
                ccc= "主动技能" if v['is_skill']==1 else "被动技能"
                desc='''<html><head><body><div style="font:18px Microsoft YaHei; color:rgb(168,94,35);max-width: 100px;" >{}</div>
                <div style="font:15px Microsoft YaHei; color:#00aeff;max-width: 100px;" >{}</div><div style="color:rgb(168,94,35)">------------------------------------</div>
                <div style="font:15px Microsoft YaHei; color:rgb(168,94,35);max-width: 100px;" >{}</div></body></html>'''.format(v['name'],ccc,v['desc'])
                
                self.qxComboBox.addItem(QtGui.QIcon("../artResources/qiXueImg/{}/{}.png".format(self.PRO[0],v['icon'])),'\n'.join(v['name']),("a tooltip",Qt.ToolTipRole))
                self.qxComboBox.setItemData(ind,_translate('self',desc),QtCore.Qt.ToolTipRole)

                ind+=1
    
    # 奇穴事件    
    def qiXueEvent(self,obj):
        op=obj.parent()
        for qxComboBox in op.findChildren(QtWidgets.QComboBox):
            print(qxComboBox.currentIndex())
        # print(obj.currentIndex())

    # 秘籍UI
    def rareBookUI(self):
        self.rbFrame = QtWidgets.QFrame(self.Calculators, objectName='rbFrame')
        self.rbFrame.setGeometry(QtCore.QRect(10, 950, 600, 170))
        self.rbFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rbFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.rbTitleFrame = QtWidgets.QFrame(self.rbFrame)
        self.rbTitleFrame.setGeometry(QtCore.QRect(0, 0, 28, 170))
        self.rbTitleLabel = QtWidgets.QLabel(
            self.rbTitleFrame, objectName='rbTitleLabel')
        self.rbTitleLabel.setGeometry(QtCore.QRect(0, 0, 28, 170))
        self.rbTitleLabel.setAlignment(Qt.AlignCenter)
        self.rbTitleLabel.setText('秘\n籍')

        rbboxxy = [(26, 0, 574, 34), (26, 34, 574, 34),
                   (26, 68, 574, 34), (26, 102, 574, 34), (26, 136, 574, 34)]
        # for fi,fm in enumerate(rbboxxy,1):
        rarabooks=Configure.GameConf().getRarabooks()
        for fi in range(len(rarabooks)):
            self.rbbox = QtWidgets.QGroupBox(self.rbFrame)
            self.rbbox.setGeometry(QtCore.QRect(*rbboxxy[fi]))
            # self.rbbox.setFrameShape(QtWidgets.QFrame.StyledPanel)
            # self.rbbox.setFrameShadow(QtWidgets.QFrame.Raised)
            self.rbbox.setObjectName("rbbox_{}".format(str(fi+1).zfill(2)))

            self.rbHorizontalLayoutWidget = QtWidgets.QWidget(self.rbbox)
            self.rbHorizontalLayoutWidget.setGeometry(
                QtCore.QRect(50, 2, 522, 30))
            self.rbHorizontalLayoutWidget.setObjectName(
                "rbHorizontalLayoutWidget_{}".format(str(fi+1).zfill(2)))
            self.rbHorizontalLayout = QtWidgets.QHBoxLayout(
                self.rbHorizontalLayoutWidget)
            self.rbHorizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.rbHorizontalLayout.setObjectName(
                "rbHorizontalLayout_{}".format(str(fi+1).zfill(2)))

        c = 1
        arbxy = [(5, 0, 40, 30)]
        for k, v in rarabooks.items():
            lableobjname = 'rbbox_{}'.format(str(c).zfill(2))
            lableobj = self.rbFrame.findChild(
                QtWidgets.QGroupBox, lableobjname)
            hobjname1 = 'rbHorizontalLayoutWidget_{}'.format(str(c).zfill(2))
            hobj1 = self.rbFrame.findChild(
                QtWidgets.QWidget, hobjname1)
            hobjname2 = 'rbHorizontalLayout_{}'.format(str(c).zfill(2))

            hobj2 = self.rbFrame.findChild(
                QtWidgets.QHBoxLayout, hobjname2)
            for z, vv in enumerate(v, 1):
                self.rbcheckBox = QtWidgets.QCheckBox(parent=hobj1)
                self.rbcheckBox.setObjectName(
                    "rbcheckBox_{}".format(str(z).zfill(2)))
                hobj2.addWidget(self.rbcheckBox)
                self.rbcheckBox.setText(vv)
                self.rbcheckBox.stateChanged.connect(
                    partial(self.rareBookEvent, self.rbcheckBox))

            self.arb = QtWidgets.QLabel(lableobj, objectName='arb')
            self.arb.setGeometry(QtCore.QRect(0, 2, 50, 32))
            self.arb.setAlignment(Qt.AlignCenter)
            self.arb.setText(k)
            c += 1
            
    # 秘籍事件,选择4本后其余的不可选
    def rareBookEvent(self, obj):
        groupbox = obj.parent()
        zt = 0
        for checkbox in groupbox.findChildren(QtWidgets.QCheckBox):
            if checkbox.isChecked():
                zt += 1
        if zt >= 4:
            for checkbox in groupbox.findChildren(QtWidgets.QCheckBox):
                if not checkbox.isChecked():
                    checkbox.setEnabled(False)
        else:
            for checkbox in groupbox.findChildren(QtWidgets.QCheckBox):
                checkbox.setEnabled(True)

        # 获取了所有秘籍的QGroupBox对象
        for x in groupbox.parent().parent().findChildren(QtWidgets.QGroupBox):
            print(x.objectName())

    # 增益UI
    def buffBoxUI(self):
        self.bbFrame = QtWidgets.QFrame(self.Calculators, objectName='bbFrame')
        self.bbFrame.setGeometry(QtCore.QRect(630, 710, 1010, 410))
        self.bbFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bbFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.zyLabel = QtWidgets.QLabel(self.bbFrame, objectName='zyLabel')
        self.zyLabel.setGeometry(QtCore.QRect(20, 10, 150, 20))
        self.zyLabel.setText('增益选择')

        self.useBuff = QtWidgets.QCheckBox(self.bbFrame, objectName='useBuff')
        self.useBuff.setGeometry(QtCore.QRect(870, 10, 150, 20))
        self.useBuff.setText('是否计算增益')

        xcxynames,yxnames, cjnames, mbnames, ewnames, tsnames =Configure.GameConf().getBuffs()
        
        # 单体
        self.fxcfxyGroupBox = QtWidgets.QGroupBox(
            self.bbFrame, objectName='fxcfxyGroupBox')
        self.fxcfxyGroupBox.setGeometry(QtCore.QRect(10, 35, 990, 90))
        self.fxcfxyLabel = QtWidgets.QLabel(
            self.fxcfxyGroupBox, objectName='fxcfxyLabel')
        self.fxcfxyLabel.setGeometry(QtCore.QRect(10, 0, 20, 90))
        self.fxcfxyLabel.setText('单\n体')
        self.fxcfxyLabel.setStyleSheet('#fxcfxyLabel{color:rgb(42,121,255)}')
        xcxynaxy = [(40, 20), (282, 20), (524, 20), (766, 20),
                    (40, 50), (282, 50), (524, 50)]
        for i, n in enumerate(xcxynames, 1):
            self.xcxynaLabel = QtWidgets.QLabel(
                self.fxcfxyGroupBox, objectName='xcxynaLabel')
            self.xcxynaLabel.setGeometry(QtCore.QRect(*xcxynaxy[i-1], 70, 25))
            self.xcxynaLabel.setText(n)

            # self.xcxynaComboBox = QtWidgets.QComboBox(self.fxcfxyGroupBox,objectName='xcxynaComboBox_{}'.format(str(i).zfill(2)))
            self.xcxynaComboBox = ExtendedComboBox(self.fxcfxyGroupBox)
            self.xcxynaComboBox.setObjectName(
                'xcxynaComboBox_{}'.format(str(i).zfill(2)))
            xx, yy = xcxynaxy[i-1]
            self.xcxynaComboBox.setGeometry(QtCore.QRect(xx+70, yy, 150, 30))
            # self.xcxynaComboBox.addItems(['断浪·上品凝神散', '断浪·中品破秽散', '断浪·玉笛谁家听落梅'])
            # 添加选项提示
            # self.xcxynaComboBox.setItemData(0,"紫破招(222点)",Qt.ToolTipRole)

        # 宴席
        self.yxGroupBox = QtWidgets.QGroupBox(
            self.bbFrame, objectName='yxGroupBox')
        self.yxGroupBox.setGeometry(QtCore.QRect(10, 130, 990, 40))
        self.yxLabel = QtWidgets.QLabel(self.yxGroupBox, objectName='yxLabel')
        self.yxLabel.setGeometry(QtCore.QRect(10, 0, 20, 40))
        self.yxLabel.setText('宴\n席')
        self.yxLabel.setStyleSheet('#yxLabel{color:rgb(42,121,255)}')
        yxxy = [(40, 10), (210, 10), (380, 10), (550, 10), (720, 10)]
        for yxi, yxn in enumerate(yxnames, 1):
            self.yxCheckBox = QtWidgets.QCheckBox(
                self.yxGroupBox, objectName='yxCheckBox_{}'.format(str(yxi).zfill(2)))
            self.yxCheckBox.setGeometry(QtCore.QRect(*yxxy[yxi-1], 160, 20))
            self.yxCheckBox.setText(yxn)

        # 常见
        self.cjGroupBox = QtWidgets.QGroupBox(
            self.bbFrame, objectName='cjGroupBox')
        self.cjGroupBox.setGeometry(QtCore.QRect(10, 175, 990, 40))
        # self.yxGroupBox.setGeometry(QtCore.QRect(10, 130, 990, 40))
        self.cjLabel = QtWidgets.QLabel(self.cjGroupBox, objectName='cjLabel')
        self.cjLabel.setGeometry(QtCore.QRect(10, 0, 20, 40))
        self.cjLabel.setText('常\n见')
        self.cjLabel.setStyleSheet('#cjLabel{color:rgb(42,121,255)}')
        cjxy = [(40, 10), (290, 10)]
        for cji, cjn in enumerate(cjnames, 1):
            self.yxCheckBox = QtWidgets.QCheckBox(
                self.cjGroupBox, objectName='yxCheckBox_{}'.format(str(cji).zfill(2)))
            self.yxCheckBox.setGeometry(QtCore.QRect(*cjxy[cji-1], 200, 20))
            self.yxCheckBox.setText(cjn)

        # 目标
        self.mbGroupBox = QtWidgets.QGroupBox(
            self.bbFrame, objectName='mbGroupBox')
        self.mbGroupBox.setGeometry(QtCore.QRect(10, 220, 990, 40))
        # self.yxGroupBox.setGeometry(QtCore.QRect(10, 130, 990, 40))
        self.mbLabel = QtWidgets.QLabel(self.mbGroupBox, objectName='mbLabel')
        self.mbLabel.setGeometry(QtCore.QRect(10, 0, 20, 40))
        self.mbLabel.setText('目\n标')
        self.mbLabel.setStyleSheet('#mbLabel{color:rgb(42,121,255)}')
        mbxy = [(40, 10), (290, 10), (490, 10), (690, 10)]
        for mbi, mbn in enumerate(mbnames, 1):
            self.yxCheckBox = QtWidgets.QCheckBox(
                self.mbGroupBox, objectName='yxCheckBox_{}'.format(str(mbi).zfill(2)))
            self.yxCheckBox.setGeometry(QtCore.QRect(*mbxy[mbi-1], 200, 20))
            self.yxCheckBox.setText(mbn)

        # 额外
        self.ewGroupBox = QtWidgets.QGroupBox(
            self.bbFrame, objectName='ewGroupBox')
        self.ewGroupBox.setGeometry(QtCore.QRect(10, 260, 990, 90))
        self.ewLabel = QtWidgets.QLabel(self.ewGroupBox, objectName='ewLabel')
        self.ewLabel.setGeometry(QtCore.QRect(10, 0, 20, 90))
        self.ewLabel.setText('额\n外')
        self.ewLabel.setStyleSheet('#ewLabel{color:rgb(42,121,255)}')
        ewxy = [(40, 10), (195, 10), (350, 10), (505, 10), (660, 10), (815, 10),
                (40, 45), (195, 45), (350, 45), (505, 45), (660, 45), (815, 45)]
        for ewi, ewn in enumerate(ewnames, 1):
            self.ewLabel = QtWidgets.QLabel(
                self.ewGroupBox, objectName='ewLabel')
            self.ewLabel.setGeometry(QtCore.QRect(*ewxy[ewi-1], 70, 25))
            self.ewLabel.setText(ewn)
            self.ewLabel.setAlignment((Qt.AlignCenter))

            self.ewLineEdit = QtWidgets.QLineEdit(self.ewGroupBox)
            self.ewLineEdit.setObjectName(
                'ewLineEdit_{}'.format(str(ewi).zfill(2)))
            ewxx, ewyy = ewxy[ewi-1]
            self.ewLineEdit.setGeometry(QtCore.QRect(ewxx+70, ewyy, 70, 30))

        # 特殊
        self.tsGroupBox = QtWidgets.QGroupBox(
            self.bbFrame, objectName='tsGroupBox')
        self.tsGroupBox.setGeometry(QtCore.QRect(10, 355, 990, 50))
        self.tsLabel = QtWidgets.QLabel(self.tsGroupBox, objectName='tsLabel')
        self.tsLabel.setGeometry(QtCore.QRect(10, 0, 20, 50))
        self.tsLabel.setText('特\n殊')

        self.tsLabel.setStyleSheet('#tsLabel{color:rgb(42,121,255)}')
        tsxy = [(40, 10), (340, 10), (640, 10)]
        for tsi, tsn in enumerate(tsnames, 1):
            self.tsLabel = QtWidgets.QLabel(
                self.tsGroupBox, objectName='tsLabel')
            self.tsLabel.setGeometry(QtCore.QRect(*tsxy[tsi-1], 70, 25))
            self.tsLabel.setText(tsn)
            self.tsLabel.setAlignment((Qt.AlignCenter))

            self.tsLineEdit_fg = QtWidgets.QLineEdit(self.tsGroupBox)
            self.tsLineEdit_fg.setObjectName(
                'tsLineEdit_fg_{}'.format(str(tsi).zfill(2)))
            tsxx, tsyy = tsxy[tsi-1]
            self.tsLineEdit_fg.setGeometry(QtCore.QRect(tsxx+70, tsyy, 70, 30))

            self.tsLineEdit_cs = QtWidgets.QLineEdit(self.tsGroupBox)
            self.tsLineEdit_cs.setObjectName(
                'tsLineEdit_cs_{}'.format(str(tsi).zfill(2)))
            tsxx, tsyy = tsxy[tsi-1]
            self.tsLineEdit_cs.setGeometry(
                QtCore.QRect(tsxx+150, tsyy, 50, 30))

        self.tsLabel01 = QtWidgets.QLabel(
            self.ewGroupBox, objectName='tsLabel01')
        self.tsLabel01.setGeometry(QtCore.QRect(970, 8, 15, 15))
        self.tsLabel01.setStyleSheet(
            '#tsLabel01{border-image:url(../artResources/defaultLattice/tsts.png);}')
        self.ewGroupBox.setToolTip("Tip:输入0-100，表示全程覆盖百分比，\n0或空为无此增益")
        self.tsLabel02 = QtWidgets.QLabel(
            self.tsGroupBox, objectName='tsLabel02')
        self.tsLabel02.setGeometry(QtCore.QRect(970, 8, 15, 15))
        self.tsLabel02.setStyleSheet(
            '#tsLabel02{border-image:url(../artResources/defaultLattice/tsts.png);}')
        self.tsGroupBox.setToolTip(
            "Tip:\n前一个框输入0-100，表示全程覆盖百分比，\n0或空为无此增益，\n后一个框表示层数")


if __name__ == '__main__':
    import sys
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    from qt_material import apply_stylesheet
    apply_stylesheet(app, theme='light_blue.xml')
    # apply_stylesheet(app, theme='dark_teal.xml')

    MainWindow = QtWidgets.QMainWindow()
    
    styleFile = '../CQss/'
    qssStyle = tools.CommonHelper.readQsss(styleFile)

    MainWindow.setStyleSheet(qssStyle)
    ui = CalculatorUI(MainWindow)

    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


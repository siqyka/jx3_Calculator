from PyQt5.QtWidgets import QStyle, QComboBox, QLineEdit, QApplication,QStyleOptionComboBox
import sys
# from ExtendedTools import ExtendedComboBox
# class aa():
#     def run(self):
#         app = QApplication(sys.argv)
#         self.win = ExtendedComboBox()
#         self.win.arrowClicked.connect(self.scan_printer_list_slot)   
#         l = ["", "1aew","2asd","3ewqr","3ewqc","2wqpu","1kjijhm", "4kjndw", "5ioijb","6eolv", "11ofmsw"]
#         self.win.addItems(l)
#         self.win.show()
#         sys.exit(app.exec_())
        
        
#     def scan_printer_list_slot(self):
#             print("扫描打印机并刷新列表")
    
# if __name__ == '__main__':
#     aa().run()

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget

class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.handle_clicked)

    def handle_clicked(self):
        print("Clicked")

app = QApplication(sys.argv)

combo = ComboBox()
combo.addItems(["Item 1", "Item 2", "Item 3"])

layout = QVBoxLayout()
layout.addWidget(combo)

window = QWidget()
window.setLayout(layout)
window.show()

sys.exit(app.exec_())

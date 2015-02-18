# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\usr\local\py\bloomberg\charts.ui'
#
# Created: Tue Feb  3 12:17:53 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(544, 452)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 531, 351))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.widget = QtGui.QWidget(self.tab)
        self.widget.setGeometry(QtCore.QRect(0, 0, 521, 331))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.widget_2 = QtGui.QWidget(self.tab_2)
        self.widget_2.setGeometry(QtCore.QRect(0, 0, 521, 331))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(250, 420, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalSlider = QtGui.QSlider(Dialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(370, 370, 161, 31))
        self.horizontalSlider.setMaximum(3)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(0)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(360, 400, 31, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Narrow"))
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(420, 400, 21, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Narrow"))
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(470, 400, 21, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Narrow"))
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(520, 400, 21, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Narrow"))
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 370, 321, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textBrowser.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Charts", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Price", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Log Price", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Returns", None))
        self.okButton.setText(_translate("Dialog", "Ok", None))
        self.label.setText(_translate("Dialog", "max", None))
        self.label_2.setText(_translate("Dialog", "1y", None))
        self.label_3.setText(_translate("Dialog", "6m", None))
        self.label_4.setText(_translate("Dialog", "1m", None))


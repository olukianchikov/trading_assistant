# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\usr\local\py\bloomberg\dates_stocks.ui'
#
# Created: Sun Feb  1 00:27:55 2015
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(521, 354)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 40, 211, 271))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 341, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(260, 10, 231, 301))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(40, 110, 181, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(40, 50, 181, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 200, 201, 41))
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.dateEdit_2 = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_2.setGeometry(QtCore.QRect(40, 130, 181, 22))
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.dateEdit = QtGui.QDateEdit(self.groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(40, 70, 181, 22))
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(20, 20, 171, 17))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 170, 82, 17))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.spinDateBox = QtGui.QDateEdit(self.groupBox)
        self.spinDateBox.setGeometry(QtCore.QRect(40, 250, 181, 22))
        self.spinDateBox.setObjectName(_fromUtf8("spinDateBox"))
        self.lcdNumber = QtGui.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(20, 320, 64, 23))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(90, 320, 131, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(420, 320, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 320, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_2.setText(_translate("Form", "Click on stocks that you want to include:", None))
        self.groupBox.setTitle(_translate("Form", "Select time frame for in-sample testing", None))
        self.label_3.setText(_translate("Form", "End date for in-sample testing:", None))
        self.label.setText(_translate("Form", "Start dates for in-sample testing:", None))
        self.label_4.setText(_translate("Form", "Only data from the selected month over all the years will be used for in-sample testing:", None))
        self.radioButton.setText(_translate("Form", "From-To time period", None))
        self.radioButton_2.setText(_translate("Form", "Month name", None))
        self.label_5.setText(_translate("Form", "stocks selected", None))
        self.pushButton.setText(_translate("Form", "Analyze", None))
        self.pushButton_2.setText(_translate("Form", "Back", None))


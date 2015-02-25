# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\usr\local\py\bloomberg\gui.ui'
#
# Created: Sun Feb  1 00:27:34 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(466, 270)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.outputScreen = QtGui.QTextBrowser(self.centralwidget)
        self.outputScreen.setGeometry(QtCore.QRect(10, 480, 451, 81))
        self.outputScreen.setObjectName(_fromUtf8("outputScreen"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 451, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.bigDataLoad = QtGui.QPushButton(self.groupBox)
        self.bigDataLoad.setGeometry(QtCore.QRect(10, 60, 75, 23))
        self.bigDataLoad.setObjectName(_fromUtf8("bigDataLoad"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(320, 20, 71, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.progressBar = QtGui.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(QtCore.QRect(200, 20, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 421, 31))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 60, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 150, 451, 291))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.strategyComboBox = QtGui.QComboBox(self.groupBox_2)
        self.strategyComboBox.setGeometry(QtCore.QRect(20, 50, 211, 22))
        self.strategyComboBox.setObjectName(_fromUtf8("strategyComboBox"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 191, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.csvLoad = QtGui.QPushButton(self.groupBox_2)
        self.csvLoad.setGeometry(QtCore.QRect(320, 210, 75, 23))
        self.csvLoad.setObjectName(_fromUtf8("csvLoad"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 260, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 90, 411, 81))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.radioButton = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 171, 20))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 50, 271, 17))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(20, 210, 281, 22))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 101, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 483, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_portfolio = QtGui.QAction(MainWindow)
        self.actionSave_portfolio.setObjectName(_fromUtf8("actionSave_portfolio"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionSave_portfolio)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.csvLoad, QtCore.SIGNAL(_fromUtf8("clicked()")), self.outputScreen.reload)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Parse Data File", None))
        self.bigDataLoad.setText(_translate("MainWindow", "Choose File", None))
        self.label.setText(_translate("MainWindow", "Completed.", None))
        self.label_3.setText(_translate("MainWindow", "If you have big excel file with various types of data, you can parse it into more suitable .csv files with prices", None))
        self.pushButton.setText(_translate("MainWindow", "Skip", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Strategy", None))
        self.label_2.setText(_translate("MainWindow", "Choose trading strategy from the list:", None))
        self.csvLoad.setText(_translate("MainWindow", "Load", None))
        self.pushButton_2.setText(_translate("MainWindow", "Next", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Select one of the options:", None))
        self.radioButton.setText(_translate("MainWindow", "Include all stocks for analysis", None))
        self.radioButton_2.setText(_translate("MainWindow", "Let me choose what stocks to include into analysis", None))
        self.lineEdit.setText(_translate("MainWindow", "No file loaded", None))
        self.label_5.setText(_translate("MainWindow", "File with stock data:", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionSave_portfolio.setText(_translate("MainWindow", "Save portfolio", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))


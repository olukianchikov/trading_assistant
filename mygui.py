from gui import *
import gui as gui
from stock_dates_form import *
import sys, time
import model as m
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import datetime
import matplotlib.pyplot as plt
from charts import *
from matplotlib.finance import fetch_historical_yahoo
from matplotlib.finance import parse_yahoo_historical_ochl
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
import matplotlib.gridspec as gridspec
import matplotlib
import math
import numpy as np
import matplotlib.dates as mdates
import analysis as an

import urllib

class MyGui(Ui_MainWindow, QMainWindow):
    progressChanged = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(MyGui, self).__init__(parent)
        self.setupUi(self)
        self.bigDataLoad.clicked.connect(self.openFileDialog)
        self.csvLoad.clicked.connect(self.loadCsvDialog)
        self.__model = m.Model()   # we will remember a model instance
        self.__workers = []
        self.connect(self, SIGNAL("progressChanged()"), self.changeProgressBar)
        self.progress = 0   # set initial progress bar value
        self.progressBar.setValue(0)
        self.label.setVisible(False)
        self.setWindowIcon(QtGui.QIcon("G:\\usr\\local\py\\bloomberg\\icon.png"))
        self.setWindowTitle("Trader Assistant")
        self.groupBox_2.hide()
        self.nextButton = QtGui.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(360, 60, 75, 23))
        self.nextButton.setObjectName(gui._fromUtf8("nextButton"))
        self.nextButton.setText(gui._translate("MainWindow", "Next", None))
        self.nextButton.clicked.connect(lambda: self.display_error("Fuck"))
        self.pushButton.clicked.connect(self.skip_parsing)
        self.outputScreen.setReadOnly(True)
        self.more_button = QtGui.QToolButton(self.groupBox_2)
        self.more_button.setGeometry(QtCore.QRect(405, 50, 30, 24))
        self.more_button.setIcon(QtGui.QIcon("G:\\usr\\local\py\\bloomberg\\question.png"))
        self.more_button.clicked.connect(self.display_description)
        #self.more_button.setObjectName(gui._fromUtf8("more"))
        self.more_button.setVisible(False)
        font = self.outputScreen.font()
        font.setFamily("Courier")
        font.setPointSize(9)
        self.sb = self.outputScreen.verticalScrollBar()
        self.first_window()
        self.all_stocks = True    # It will be set by radio button
        self.pushButton_2.clicked.connect(self.move_to_window3)
        self.selected_strategy_index = 0
        self.stock_names = []
        self.actionExit.triggered.connect(self.close)
        self.checkBox_long = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_long.setGeometry(QtCore.QRect(30, 90, 20, 20))
        self.label_check_1 = QtGui.QLabel(self.groupBox_2)
        self.label_check_1.setGeometry(QtCore.QRect(50, 90, 60, 20))
        self.label_check_1.setText("Long only")
        self.checkBox_two_entries = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_two_entries.setGeometry(QtCore.QRect(180, 90, 20, 20))
        self.label_check_2 = QtGui.QLabel(self.groupBox_2)
        self.label_check_2.setGeometry(QtCore.QRect(200, 90, 80, 20))
        self.label_check_2.setText("Two entries")

    def close(self):
        QtCore.QCoreApplication.instance().quit()

    def openFileDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(QFileDialog(), 'Open xlsx file with stock prices', '', "Excel files (*.xlsx)")
        try:
            if fname is not "":
                self.changeProgressBar(0)   # Flush it before we started the thread.
                self.startNewWorker(self.__model.handleXlsx, fname, os.getcwd(), self.notify_progress_change)
                self.display_message("Parsing of the file started.")
        except Exception as x:
            self.display_error(str(x))

    def startNewWorker(self, function, *args, **kwargs):
        if len(self.__workers) > 1:
            raise Exception("sorry, the work is being in progress, just wait until it's done.")
        self.__workers.append(WorkThread(function, args, kwargs))
        self.connect(self.__workers[0], SIGNAL("finished()"), self.workerFinished)
        self.__workers[0].terminated.connect(lambda:  self.workerFinished("Parsing aborted."))
        #self.connect(self.__workers[0], SIGNAL("terminated()"), self.workerFinished)
        self.__workers[0].start()
        self.changeProgressBar(1)

    def workerFinished(self, text="Done."):
        """Method is called when the worher thread finnished it's job."""
        self.display_message(text)
        del self.__workers[0]

    def loadCsvDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open csv file with stock prices','', "CSV data files (*.csv)")
        self.lineEdit.setText(fname)
        return fname

    def display_error(self, error_message):
        self.outputScreen.moveCursor(QTextCursor.End)
        redColor = QColor(255, 20, 20)
        self.outputScreen.setTextColor(redColor)
        self.outputScreen.append(error_message)
        QScrollBar.setValue(self.sb, self.sb.maximum())
        #self.sb.setVaue(self.sb.maximum())

    def display_message(self, message):
        self.outputScreen.moveCursor(QTextCursor.End)
        greenColor = QColor(20, 250, 20)
        self.outputScreen.setTextColor(greenColor)
        self.outputScreen.append(message)
        QScrollBar.setValue(self.sb, self.sb.maximum())

    def notify_progress_change(self, progress_value):
        """TO emit the signal that the progress bar must catch."""
        self.progress = progress_value
        self.progressChanged.emit()

    def skip_parsing(self):
        if len(self.__workers) == 1:
            answer = self.ask_to_confirm("Are you really sure you want to abort parsing the file now?")
            if answer == QtGui.QMessageBox.Yes:
                self.__workers[0].terminated.emit()
        else:
            self.first_window_hide()
            self.window2()

    def first_window_hide(self):
        self.groupBox.hide()
        self.progressBar.hide()
        self.pushButton.hide()
        self.nextButton.hide()

    def first_window(self):
        """Sets position and dimentions for first window. Here window is more like what user see, not an object."""
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 451, 141))
        initial_win_size_width = self.groupBox.geometry().width() + 15
        initial_win_size_height = self.groupBox.geometry().height() + self.progressBar.geometry().height() + 20
        initial_win_size_height += self.outputScreen.geometry().height() + 5
        #print(initial_win_size_width, initial_win_size_height)
        self.setFixedSize(initial_win_size_width, initial_win_size_height)
        self.progressBar.setGeometry(QtCore.QRect(10, self.groupBox.geometry().bottom()-45, 445, 20))
        self.outputScreen.setGeometry(QtCore.QRect(10, self.groupBox.geometry().bottom()+5, 451, 40))
        self.pushButton.setGeometry(QtCore.QRect(305, self.groupBox.geometry().bottom()+55, 75, 23))
        self.nextButton.setGeometry(QtCore.QRect(385, self.groupBox.geometry().bottom()+55, 75, 23))
        self.nextButton.setEnabled(False)
        #self.nextButton.setEnabled(False)

    def window2(self):
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 460, 285))
        self.setFixedSize(480, 415)
        self.csvLoad.setGeometry(QtCore.QRect(320, 210, 35, 24))
        self.csvLoad.setText("")
        self.csvLoad.setIcon(QtGui.QIcon("G:\\usr\\local\py\\bloomberg\\open.png"))
        self.strategyComboBox.setGeometry(QtCore.QRect(20, 50, 380, 24))
        self.label_5.setGeometry(QtCore.QRect(20, 220, 101, 16))
        self.lineEdit.setGeometry(QtCore.QRect(20, 240, 281, 24))
        self.csvLoad.setGeometry(QtCore.QRect(320, 240, 75, 23))
        self.outputScreen.setGeometry(QtCore.QRect(10, self.groupBox_2.geometry().bottom()+5, 460, 40))
        self.pushButton_2.setGeometry(QtCore.QRect(395, self.outputScreen.geometry().bottom()+5, 75, 23))
        strategies = self.__model.get_strategies()
        self.strategyComboBox.addItems(strategies)
        self.more_button.setVisible(True)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 120, 411, 81))
        self.lineEdit.setPlaceholderText("No file loaded")
        self.lineEdit.setText("")
        self.radioButton.setText("Don't fill in missing values")
        self.radioButton_2.setText("Fill in missing prices with last available prices")
        self.radioButton.setChecked(True)
        self.radioButton_2.setChecked(False)
        self.pushButton_2.show()
        self.groupBox_2.show()

    def move_to_window3(self):
        self.selected_strategy_index = self.strategyComboBox.currentIndex()
        self.stock_names = self.__model.load_names_from_csv(self.lineEdit.text())
        self.date_form = DateForm(self)
        if self.lineEdit.text() is not "":
            """We have set csv file"""
            first_date = self.__model.load_first_date_from_csv(self.lineEdit.text())
            self.date_form.dateEdit.setDate(QDate(first_date.year, first_date.month, first_date.day))
            last_date = self.__model.load_last_date_from_csv(self.lineEdit.text())
            self.date_form.dateEdit_2.setDate(QDate(last_date.year, last_date.month, last_date.day))
            names = self.__model.load_names_from_csv(self.lineEdit.text())
            for i in range(0, len(names)):
                self.date_form.listWidget.addItem(names[i])
            self.date_form.add_button.setVisible(False)
            self.date_form.lineEdit.setVisible(False)
            self.date_form.listWidget.setGeometry(QtCore.QRect(20, 40, 211, 271))
            self.date_form.setCsv(self.lineEdit.text())
        else:
            """No csv file set. Entering Yahoo Finance mode"""
            self.date_form.add_button.setVisible(True)
            self.date_form.lineEdit.setVisible(True)
            self.date_form.listWidget.setGeometry(QtCore.QRect(20, 60, 211, 241))
            self.date_form.setCsv(None)
        self.date_form.radioButton.setChecked(True)
        self.groupBox_2.hide()
        self.pushButton_2.hide()
        self.outputScreen.hide()
        self.date_form.show()
        self.date_form.pushButton_2.clicked.connect(self.from3_to_win2)
        self.date_form.pushButton.clicked.connect(self.analyze)
        self.setFixedSize(531, 374)

    def analyze(self, ffile = None):
        list_sec = self.date_form.listWidget.selectedItems()
        for i in range(0, len(list_sec)):
            list_sec[i] = list_sec[i].text()   # contains a list of names of selected assets
        results = self.__model.create_strategy(self.strategyComboBox.currentIndex(), list_sec, self.lineEdit.text()) # WHAT IF ITS EMPTY? IT CAUSES AN ERROR!
        self.analysisDialog = AnalysisDialog(self)
        text_2_show = ""
        text_2_show += "The results of the analysis of {} securities:\n".format(len(results[0]))
        text_2_show += "The strategy is: {}\n".format(self.strategyComboBox.currentText())
        text_2_show += "To implement this strategy you should enter the following positions:\n"
        for j in range(0, len(results[0])):
            text_2_show += "{}: {}\n".format(results[0][j], results[1][j])
        self.analysisDialog.output.setText(text_2_show)
        self.analysisDialog.show()


    def from3_to_win2(self):
        self.date_form.hide()
        self.window2()


    def display_description(self, index):
         index = self.strategyComboBox.currentIndex()
         help = QMessageBox.information(self, "Help", self.__model.get_strategy_descriptions()[index],\
                                        QtGui.QMessageBox.Ok)

    def ask_to_confirm(self, question):
        answer = QMessageBox.question(self, \
                            "Warning",\
                            question, \
                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        print(type(answer))
        print(answer)
        return answer

    def changeProgressBar(self, value=None):
        if value is None:
            our_value = self.progress
        else:
            our_value = value
        self.progressBar.setValue(our_value)
        if our_value is 100:
            self.nextButton.setEnabled(True)
            self.display_message("File parsing completed successfully!")
            self.pushButton.setEnabled(False)
            self.bigDataLoad.setEnabled(True)
        elif our_value is 0:
            self.bigDataLoad.setEnabled(True)
        else:
            self.nextButton.setEnabled(False)
            self.pushButton.setEnabled(True)
            self.bigDataLoad.setEnabled(False)

class DateForm(Ui_Form, QtGui.QWidget):
    def __init__(self, parent=MyGui):
        super(DateForm, self).__init__(parent)
        self.setupUi(self)
        self.listWidget.itemSelectionChanged.connect(self.set_num_stocks)
        palette = self.lcdNumber.palette()
        palette.setColor(palette.WindowText, QtGui.QColor(85, 85, 255))
        #palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        palette.setColor(palette.Light, QtGui.QColor(93, 93, 93))
        palette.setColor(palette.Dark, QtGui.QColor(190, 190, 190))
        self.lcdNumber.setPalette(palette)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setGeometry(10, 20, 521, 354)
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.listItemRightClicked)
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 60, 24))
        self.lineEdit.setObjectName(gui._fromUtf8("lineEdit"))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText("Ticker")
        self.lineEdit.textChanged.connect(self.to_upper)
        self.add_button = QtGui.QToolButton(self)
        self.add_button.setGeometry(QtCore.QRect(85, 30, 26, 24))
        self.add_button.setIcon(QtGui.QIcon("G:\\usr\\local\py\\bloomberg\\add.png"))
        self.add_button.clicked.connect(self.add_to_list)
        self.lineEdit.returnPressed.connect(self.add_to_list)
        self.dateEdit_2.setDate(QDate.currentDate())
        self.lineEdit.setObjectName(gui._fromUtf8("add_button"))
        self.spinDateBox.setDisplayFormat("MMMM")
        self.__csv_file = None



    def setCsv(self, filename):
        self.__csv_file = filename

    def get_dates(self):
        if self.radioButton.isChecked() is True:
            beg = self.dateEdit.date()
            beg = beg.toPyDate()
            end = self.dateEdit_2.date()
            end = end.toPyDate()
        elif self.radioButton_2.isChecked() is True:
            #set no limits for beginning and end
            beg = (2005, 1, 1)
            end = datetime.date.today()
        return beg, end

    def to_upper(self):
        tex = self.lineEdit.text().upper()
        self.lineEdit.setText(tex)

    def add_to_list(self):
        if self.lineEdit.text() != '':
            self.listWidget.addItem(self.lineEdit.text())
            self.lineEdit.setText("")

    def listItemRightClicked(self, position):
        self.listWidget.listMenu = QtGui.QMenu()
        menu_item = self.listWidget.listMenu.addAction("Price charts")
        if len(self.listWidget.selectedItems()) == 0:
            menu_item.setDisabled(True)
        menu_item2 = self.listWidget.listMenu.addAction("Delete")
        if len(self.listWidget.selectedItems()) == 0:
            menu_item2.setDisabled(True)
        position_proper=QPoint()
        position_proper.setX(position.x()+20)
        position_proper.setY(position.y()+40)
        menu_item.triggered.connect(self.price_chart)
        menu_item2.triggered.connect(self.delete_item)
        self.listWidget.listMenu.popup(self.mapToGlobal(position_proper))

    def set_num_stocks(self):
        length = len(self.listWidget.selectedItems())
        self.lcdNumber.display(length)

    def price_chart(self):
        dialog = ChartsDialog(self)
        curr = self.listWidget.currentItem().text()
        beg, end = self.get_dates()
        res = dialog.set_ticker_and_dates(curr, beg, end, self.__csv_file)
        if res is True:
            dialog.draw_charts()
            dialog.show()

    def delete_item(self):
        curr = self.listWidget.currentItem()
        self.listWidget.takeItem(self.listWidget.row(curr))

class ChartsDialog(Ui_Dialog, QDialog):
    def __init__(self, parent=MyGui):
        super(ChartsDialog, self).__init__(parent)
        self.setupUi(self)
        tabWidgetX = self.tabWidget.size().width() - 3
        tabWidgetY = self.tabWidget.size().height() - 10
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), gui._translate("Dialog", "Returns", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), gui._translate("Dialog", "Unadjusted", None))
        self.okButton.clicked.connect(self.close)
        self.ticker = ""
        self.widget = matplotlibWidget(self.tab, tabWidgetX, tabWidgetY)
        self.widget_2 = matplotlibWidget(self.tab_2, tabWidgetX, tabWidgetY)
        self.widget_3 = matplotlibWidget(self.tab_3, tabWidgetX, tabWidgetY)
        self.beg = (2005, 1, 1)
        self.end = datetime.date.today()
        self.__ppp = None
        self.lookback = 0   # 0 - max, 1 - a year, 2 - 0.6 year, 3 - 1 month
        self.horizontalSlider.valueChanged.connect(self.register_lookback)
        #self.
        matplotlib.rcParams.update({'font.size': 8})
        self.__cur_widget = self.widget
        self.__y_type = "adj"
        self.tabWidget.currentChanged.connect(self.tab_changed)

    def register_lookback(self):
        self.lookback = self.horizontalSlider.value()
        if self.lookback == 0:
            date_start = self.beg
            ymin = self.__all_min
            print("ymin:{}".format(ymin))
            ymax = self.__all_max
            print("ymax:{}".format(ymax))
            yamin = self.__alla_min
            yamax = self.__alla_max
            rmax = self.__ra_max     # maximum absolute value of returns
        elif self.lookback == 1:
            date_start = self.end - datetime.timedelta(days=365)
            ymin = self.__y1_min
            ymax = self.__y1_max
            yamin =self.__y1a_min
            yamax = self.__y1a_max
            rmax = self.__ry1_max
            if date_start < self.beg:
                date_start = self.beg
        elif self.lookback == 2:
            date_start = self.end - datetime.timedelta(days=183)
            ymin = self.__m6_min
            ymax = self.__m6_max
            yamin = self.__m6a_min
            yamax = self.__m6a_max
            rmax = self.__rm6_max
            if date_start < self.beg:
                date_start = self.beg
        elif self.lookback == 3:
            date_start = self.end - datetime.timedelta(days=30)
            ymin = self.__m1_min
            ymax = self.__m1_max
            yamin = self.__m1a_min
            yamax = self.__m1a_max
            rmax = self.__rm1_max
            if date_start < self.beg:
                date_start = self.beg
        today = self.end  # In fact it should be called last_day, not today
        if (today - date_start) > datetime.timedelta(364):
            xfmt = mdates.DateFormatter('%b %Y')
        else:
            xfmt = mdates.DateFormatter('%b %d')
        self.__ax.set_xlim([date_start, today])
        self.__ax2.set_xlim([date_start, today])
        self.__ax2_1.set_xlim([date_start, today])
        self.__ax2_2.set_xlim([date_start, today])
        self.__ax4_1.set_xlim([date_start, today])
        self.__ax4_2.set_xlim([date_start, today])
        # Y limits:
        self.__ax.set_ylim([yamin*0.95, yamax*1.1]) # adjusted
        self.__ax2_1.set_ylim([ymin*0.95, ymax*1.1]) # unadjusted limits
        self.__ax4_1.set_ylim([-rmax*1.2, rmax*1.2])
        # X proper dates:
        self.__ax.xaxis.set_major_formatter(xfmt)
        self.__ax2.xaxis.set_major_formatter(xfmt)
        self.__ax2_1.xaxis.set_major_formatter(xfmt)
        self.__ax2_2.xaxis.set_major_formatter(xfmt)
        self.__ax4_1.xaxis.set_major_formatter(xfmt)
        self.__ax4_2.xaxis.set_major_formatter(xfmt)
        self.widget.canvas.draw()
        self.widget_2.canvas.draw()
        self.widget_3.canvas.draw()


    def tab_changed(self):
        """if self.tabWidget.currentIndex() == 0:
             self.__y_type = "adj"
             self.__cur_widget = self.widget
        elif self.tabWidget.currentIndex() == 1:
            self.__y_type = "close"
            self.__cur_widget = self.widget_2
        elif self.tabWidget.currentIndex() == 2:
            self.__y_type = "log_price"
            self.__cur_widget = self.widget_3
        elif self.tabWidget.currentIndex() == 3:
            self.__y_type = "return"
            self.__cur_widget = self.widget_4
        print(self.tabWidget.currentIndex())
        self.draw_chart()"""
        print(self.tabWidget.currentIndex())

    def set_ticker_and_dates(self, ticker, beg, end, ffile = None):
        p = None
        try:
            if ticker is "":
                raise Exception("Error: No ticker provided.")
            if ffile is None:
                """This will work when we use Yahoo Finance instead of csv-file:"""
                self.__ppp = m.Model.fetchStockData(beg, end, None, True, ticker)
                self.ticker = ticker
                self.beg = beg
                self.end = end
                return True
            else:
                self.__ppp = m.Model.fetchStockData(beg, end, ffile, False, ticker)
                self.ticker = ticker
                self.beg = beg
                self.end = end
                return True
        except urllib.error.HTTPError as err:
            ww = QMessageBox.critical(self, "Can't get charts", "Ticker {} cannot be found on Yahoo Finance or there "
                                                           "is a problem"\
                                                       "reaching Yahoo server. Details: \n{}".format(ticker, str(err)), QtGui.QMessageBox.Ok)
            self.ticker = ""
            self.__ppp = None
            return False
        #except Exception as errr:
        #    ww = QMessageBox.critical(self, "Can't get charts", "Details of the error:\n{}".format(str(errr)), QtGui.QMessageBox.Ok)
        #    self.ticker = ""
        #    self.__ppp = None
        #    return False

    def draw_charts(self):
        if self.__ppp is not None:
            """its a numpy array now with columns:
             date, year, month, day, d, open, close, high, low, volume, adjusted_close"""
            additional_info=""
            start = datetime.date(2000, 1, 7)
            pp = self.__ppp[self.__ppp['date'] > start]
            dates = [q[0] for q in pp]
            #dates = matplotlib.dates.date2num(dates)
            dates = np.array(dates, dtype=datetime.datetime)
            self.beg = dates[0]
            close_data = [q[6] for q in pp]
            adj_data = [q[10] for q in pp]
            #log_data = [q[10] for q in pp]
            #log_data = [math.log(y_value) for y_value in log_data]
            return_data = [q[10] for q in pp]
            return_data = np.array(return_data, dtype=np.float)
            return_data = return_data[1:]/return_data[:-1] - 1
            m = np.mean(return_data)
            sd = np.std(return_data)
            additional_info = "Mean: {} and std: {}".format(m, sd)
            volume = [q[9] for q in pp]
            # Searching for max and mins for each lookback period:
            now = datetime.date.today()
            k = 1
            self.__m1_max = 0
            self.__m1_min = 0
            self.__rm1_max = 0
            self.__m6_max = 0
            self.__m6_min = 0
            self.__rm6_max = 0
            self.__y1_max = 0
            self.__y1_min = 0
            self.__ry1_max = 0
            self.__m1a_max = 0
            self.__m1a_min = 0
            self.__m6a_max = 0
            self.__m6a_min = 0
            self.__y1a_max = 0
            self.__y1a_min = 0
            for single_date in dates[::-1]:
                if (now - single_date) > datetime.timedelta(30):
                    self.__m1_max = np.max(close_data[-1:-k:-1])
                    self.__m1_min = np.min(close_data[-1:-k:-1])
                    self.__m1a_max = np.max(adj_data[-1:-k:-1])
                    self.__m1a_min = np.min(adj_data[-1:-k:-1])
                    self.__rm1_max = np.max(np.absolute(return_data[-1:-k:-1]))
                    break
                k += 1
            for single_date in dates[-k::-1]:
                if (now - single_date) > datetime.timedelta(183):
                    self.__m6_max = np.max(close_data[-1:-k:-1])
                    self.__m6_min = np.min(close_data[-1:-k:-1])
                    self.__m6a_max = np.max(adj_data[-1:-k:-1])
                    self.__m6a_min = np.min(adj_data[-1:-k:-1])
                    self.__rm6_max = np.max(np.absolute(return_data[-1:-k:-1]))
                    break
                k += 1
            for single_date in dates[-k::-1]:
                if (now - single_date) > datetime.timedelta(365):
                    self.__y1_max = np.max(close_data[-1:-k:-1])
                    self.__y1_min = np.min(close_data[-1:-k:-1])
                    self.__y1a_max = np.max(adj_data[-1:-k:-1])
                    self.__y1a_min = np.min(adj_data[-1:-k:-1])
                    self.__ry1_max = np.max(np.absolute(return_data[-1:-k:-1]))
                    break
                k += 1
            self.__all_max = np.max(close_data)
            print(self.__all_max)
            self.__all_min = np.min(close_data)
            print(self.__all_min)
            self.__alla_max = np.max(adj_data)
            self.__alla_min = np.min(adj_data)
            self.__ra_max = np.max(np.absolute(return_data))
            if self.__ry1_max == 0: self.__ry1_max = self.__ra_max
            if self.__y1_max == 0: self.__y1_max = self.__all_max
            if self.__y1_min == 0: self.__y1_min = self.__all_min
            if self.__m6_max == 0: self.__m6_max = self.__all_max
            if self.__m6_min == 0: self.__m6_min = self.__all_min
            if self.__rm6_max == 0: self.__rm6_max = self.__ra_max
            if self.__m1_max == 0: self.__m1_max = self.__all_max
            if self.__m1_min == 0: self.__m1_min = self.__all_min
            if self.__rm1_max == 0: self.__rm1_max = self.__ra_max

            if self.__m1a_max == 0: self.__m1a_max = self.__alla_max
            if self.__m1a_min == 0: self.__m1a_min = self.__alla_min
            if self.__m6a_max == 0: self.__m6a_max = self.__alla_max
            if self.__m6a_min == 0: self.__m6a_min = self.__alla_min
            if self.__y1a_max == 0: self.__y1a_max = self.__alla_max
            if self.__y1a_min == 0: self.__y1a_min = self.__alla_min

            print("1m max and min: {} and {}".format(self.__m1_max, self.__m1_min))
            print("6m max and min: {} and {}".format(self.__m6_max, self.__m6_min))
            print("1y max and min: {} and {}".format(self.__y1_max, self.__y1_min))

            print("1m a max and min: {} and {}".format(self.__m1a_max, self.__m1a_min))
            print("6m a max and min: {} and {}".format(self.__m6a_max, self.__m6a_min))
            print("1y a max and min: {} and {}".format(self.__y1a_max, self.__y1a_min))

            # drawing:
            gs = gridspec.GridSpec(5, 1)
            gs.update(wspace=0.00, hspace=0.00)
            # Adj Price drawing:
            self.__ax = self.widget.fig.add_subplot(gs[0:4,0])
            self.__ax.hold(False)
            self.__ax.clear()
            self.__ax.plot_date(dates, adj_data, 'b-', xdate=True)
            #ax.set_ylim([0, 200])
            self.__ax.set_title("Historical Adjusted Prices of {}".format(self.ticker))
            self.__ax.set_ylabel('Price')
            self.__ax.grid(True)
            self.__ax.axes.xaxis.set_visible(False)
            # This is if I want to draw volume:
            #ax.relim()
            #ax.autoscale_view(True, True ,True)
            xfmt = mdates.DateFormatter('%b %Y')
            self.__ax2 = self.widget.fig.add_subplot(gs[4, 0], sharex=self.__ax)
            self.__ax2.hold(False)
            self.__ax2.clear()
            self.__ax2.fill_between(dates, volume, color="b")
            self.__ax2.set_ylabel('Volume')
            self.__ax2.axes.yaxis.set_ticklabels([])
            self.__ax2.xaxis.set_major_formatter(xfmt)
            #ax2.grid(True)
            #ax2.relim()
            #ax2.autoscale_view(True,True,True)
            self.widget.fig.subplots_adjust(left=.1, bottom=.10, right=.97, wspace=0.0, hspace=0)
            #self.widget.show()
            self.widget.canvas.draw()
            # Unadjasted Price
            #
            self.__ax2_1 = self.widget_2.fig.add_subplot(gs[0:4,0])
            self.__ax2_1.hold(False)
            self.__ax2_1.clear()
            self.__ax2_1.plot_date(dates, close_data, 'b-', xdate=True)
            #ax.set_ylim([0, 200])
            self.__ax2_1.set_title("Historical Close Prices of {}".format(self.ticker))
            self.__ax2_1.set_ylabel('Price')
            self.__ax2_1.grid(True)
            self.__ax2_1.axes.xaxis.set_visible(False)
            xfmt = mdates.DateFormatter('%b %Y')
            self.__ax2_2 = self.widget_2.fig.add_subplot(gs[4, 0], sharex=self.__ax2_1)
            self.__ax2_2.hold(False)
            self.__ax2_2.clear()
            self.__ax2_2.fill_between(dates, volume, color="b")
            self.__ax2_2.set_ylabel('Volume')
            self.__ax2_2.axes.yaxis.set_ticklabels([])
            self.__ax2_2.xaxis.set_major_formatter(xfmt)
            self.widget_2.fig.subplots_adjust(left=.1, bottom=.10, right=.97, wspace=0.0, hspace=0)
            self.widget_2.canvas.draw()
            # Returns
            self.__ax4_1 = self.widget_3.fig.add_subplot(gs[0:4,0])
            self.__ax4_1.hold(False)
            self.__ax4_1.clear()
            self.__ax4_1.plot_date(dates[1:], return_data, 'b-', xdate=True)
            #ax.set_ylim([0, 200])
            self.__ax4_1.set_title("Historical Returns of {}".format(self.ticker))
            self.__ax4_1.set_ylabel('Price')
            self.__ax4_1.grid(True)
            self.__ax4_1.axes.xaxis.set_visible(False)
            xfmt = mdates.DateFormatter('%b %Y')
            self.__ax4_2 = self.widget_3.fig.add_subplot(gs[4, 0], sharex=self.__ax4_1)
            self.__ax4_2.hold(False)
            self.__ax4_2.clear()
            self.__ax4_2.fill_between(dates[1:], volume[1:], color="b")
            self.__ax4_2.set_ylabel('Volume')
            self.__ax4_2.axes.yaxis.set_ticklabels([])
            self.__ax4_2.xaxis.set_major_formatter(xfmt)
            self.widget_3.fig.subplots_adjust(left=.1, bottom=.10, right=.97, wspace=0.0, hspace=0)
            self.widget_3.canvas.draw()
        else:
            raise TypeError("Error: chart can't be drawn because the data is either empty or invalid.")

    def close(self):
        self.hide()

class matplotlibWidget(QtGui.QWidget):
    """Setting up the canvas to draw on for MatPlotLib"""
    def __init__(self, parent = None, xsize=100, ysize=100):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(xsize, ysize)
        self.vbl = QtGui.QVBoxLayout()
        my_dpi = 100
        self.fig = Figure((xsize/my_dpi, ysize/my_dpi), my_dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        #self.toolbar = NavigationToolbar(self.canvas, self)
        #self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


class WorkThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs


    def __del__(self):
        self.wait()

    def run(self):
        time.sleep(0.1)   # artificial time delay
        self.__function(self.__args[0][0], self.__args[0][1], self.__args[0][2])
        self.terminate()

class AnalysisDialog(an.Ui_Form, QDialog):
    def __init__(self, parent=MyGui):
        super(AnalysisDialog, self).__init__(parent)
        self.setupUi(self)
        self.closeButton.clicked.connect(self.hide)
        self.chartButton.clicked.connect(self.showCharts)

    def hide(self):
        self.output.setText("")
        self.setVisible(False)

    def showCharts(self):
        """Not implemented yet!"""
        raise NotImplementedError("Error: this function is not implemented yet!")

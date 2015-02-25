import sys
import PyQt4.QtGui as QtGui
import PyQt4.QtCore
import mygui
import strategies as st
import matplotlib.pyplot as plt

def main(args):
    app = QtGui.QApplication(args)
    _Font = QtGui.QFont("Tahoma", 8);
    QtGui.QApplication.setFont(_Font);
    w = mygui.MyGui()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
from PyQt5.QtWidgets import QApplication
import PySpin
from FlirCamController import FlirCamController
# from views import StartWindow
from FlirWindow import *
import matplotlib.pyplot as plt
import qdarkstyle
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

flir = FlirCamController()
flir.start_continue()
plt.imshow(flir.acquire_continue())
plt.show()

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())

flir.stop_continue()
flir.close()
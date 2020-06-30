from FlirCamController import FlirCamController
from FlirWindow import Ui_MainWindow
from FlirWindowModify import Ui_CustomWindow
import matplotlib.pyplot as plt
import qdarkstyle
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

flir = FlirCamController()
# plt.imshow(flir.acquire_continue())
# plt.show()

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
MainWindow = QtWidgets.QMainWindow()
ui = Ui_CustomWindow()
ui.cam_controller = flir
ui.setupUi(MainWindow)
ui.custom_init()

MainWindow.show()
app.exec_()
flir.stop_continue()
flir.close()
sys.exit()



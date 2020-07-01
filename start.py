from FlirCamController import FlirCamController
from FlirWindowModify import Ui_CustomWindow
from FlirCamFake import FakeCamContoller
import qdarkstyle
import sys
from PyQt5 import QtWidgets
import time

flir = FlirCamController()
# flir = FakeCamContoller()

# flir.start_continue()
# start_time = time.time()
# for i in range(100):
#     flir.acquire_continue()
# print("--- %.8f seconds ---" % (time.time() - start_time))
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



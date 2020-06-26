from PyQt5.QtWidgets import QApplication
import PySpin
from FlirCamController import FlirCamController
from views import StartWindow
import matplotlib.pyplot as plt

flir = FlirCamController()
flir.start_continue()
plt.imshow(flir.acquire_continue())
plt.show()
app = QApplication([])
start_window = StartWindow(flir)
start_window.show()
app.exit(app.exec_())

flir.stop_continue()
flir.close()
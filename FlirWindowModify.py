from PyQt5 import QtCore, QtGui, QtWidgets
from FlirWindow import Ui_MainWindow
import numpy as np
from fitgauss import fitgauss2d_section

class Ui_CustomWindow(Ui_MainWindow):
    def custom_init(self):
        # start and stop continue button
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_movie)
        self.pushButtonContinue.clicked.connect(self.start_continue)

        # Exposure Time
        self.lineEditExposureTime.setText(str(self.cam_controller.cam.ExposureTime()))
        self.lineEditExposureTime.returnPressed.connect(self.set_exptime)

    def start_continue(self):
        self.cam_controller.start_continue()
        self.pushButtonContinue.setText("Stop Continue")
        self.pushButtonContinue.clicked.disconnect()
        self.pushButtonContinue.clicked.connect(self.stop_continue)
        self.update_timer.start(50)
        # print('click')

    def stop_continue(self):
        self.update_timer.stop()
        self.cam_controller.stop_continue()
        self.pushButtonContinue.setText("Start Continue")
        self.pushButtonContinue.clicked.disconnect()
        self.pushButtonContinue.clicked.connect(self.start_continue)

    def update_movie(self):
        self.cam_controller.acquire_continue()
        xx, yy = np.meshgrid(np.arange(4000), np.arange(3000))
        p, ier = fitgauss2d_section(np.arange(0, 4000), np.arange(0, 3000), self.cam_controller.frame)
        self.lineEditxCenter.setText('%.4f' % (p[0]))
        self.lineEdityCenter.setText('%.4f' % (p[1]))
        self.lineEditxWaist.setText('%.4f' % (p[2]))
        self.lineEdityWaist.setText('%.4f' % (p[3]))
        self.lineEditHeight.setText('%.4f' % (p[4]))
        self.labelImage.setPixmap(QtGui.QPixmap(self.toQImage()))

    def toQImage(self, copy=False):
        '''
        Transfer the format of the frame from numpy.ndarray to QImage
        :param self:
        :param copy:
        :return:
        '''
        qim = QtGui.QImage(self.cam_controller.frame.data, self.cam_controller.frame.shape[1],
                           self.cam_controller.frame.shape[0], self.cam_controller.frame.strides[0],
                           QtGui.QImage.Format_Indexed8).rgbSwapped()
        # qim.setColorTable(gray_color_table)
        return qim.copy() if copy else qim

    def set_exptime(self):
        try:
            exptime = float(self.lineEditExposureTime.text())
        except ValueError as ex:
            print('ValueError: %s' % ex)
            return
        self.cam_controller.configure_exposure(exptime)



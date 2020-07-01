from PyQt5 import QtCore, QtGui
from pyqtgraph import PlotWidget
from FlirWindow import Ui_MainWindow
import numpy as np
from fitgauss import fitgauss2d_section





class Ui_CustomWindow(Ui_MainWindow):
    def custom_init(self):
        self.section_xctr = 0
        self.section_yctr = 0
        self.section_xdata = []
        self.section_ydata = []
        self.section_xcoord = []
        self.section_ycoord = []

        # init start and stop continue button
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_movie)
        self.pushButtonContinue.clicked.connect(self.start_continue)

        # init exposure time line edit
        self.lineEditExposureTime.setText(str(self.cam_controller.cam.ExposureTime()))
        self.lineEditExposureTime.returnPressed.connect(self.set_exptime)

        # init section plots
        self.plotx = PlotWidget(self.centralwidget)
        self.plotx.setObjectName("plotx")
        self.gridLayoutImage.addWidget(self.plotx, 1, 0, 1, 1)
        self.sectionx_line = self.plotx.plot(self.section_xcoord,self.section_xdata)

        self.ploty = PlotWidget(self.centralwidget)
        self.ploty.setObjectName("ploty")
        self.gridLayoutImage.addWidget(self.ploty,  0, 1, 1, 1)
        self.sectiony_line = self.ploty.plot(self.section_ydata,self.section_ycoord)

        # image label mouse press event
        self.labelImage.mousePressEvent = self.label_mousepress()

        # auto exposure check box
        self.checkBoxAutoExposure.stateChanged.connect(self.checkbox_auto_exposure)

        # background
        self.pushButtonSetBg.clicked.connect(self.set_background)
        self.pushButtonClearBg.clicked.connect(self.clear_background)

    def start_continue(self):
        self.cam_controller.start_continue()
        self.pushButtonContinue.setText("Stop Continue")
        self.pushButtonContinue.clicked.disconnect()
        self.pushButtonContinue.clicked.connect(self.stop_continue)
        # self.t0 = time.time()
        self.update_timer.start(200)
        # print('click')

    def stop_continue(self):
        self.update_timer.stop()
        # print("--- %.8f seconds ---" % (time.time() - self.t0))
        # print("no frames : %d"%(self.cam_controller.framecount))
        self.cam_controller.stop_continue()
        self.pushButtonContinue.setText("Start Continue")
        self.pushButtonContinue.clicked.disconnect()
        self.pushButtonContinue.clicked.connect(self.start_continue)

    def update_movie(self):
        self.cam_controller.acquire_continue()
        self.update_plot()
        p, ier = fitgauss2d_section(np.arange(0, self.cam_controller.frame.shape[1]),
                                    np.arange(0, self.cam_controller.frame.shape[0]), self.cam_controller.frame)
        self.lineEditxCenter.setText('%.4f' % (p[0]))
        self.lineEdityCenter.setText('%.4f' % (p[1]))
        self.lineEditxWaist.setText('%.4f' % (p[2]))
        self.lineEdityWaist.setText('%.4f' % (p[3]))
        self.lineEditHeight.setText('%.4f' % (p[4]))
        self.labelImage.setPixmap(QtGui.QPixmap(self.toQImage()))
        if self.checkBoxAutoExposure.isChecked():
            self.lineEditExposureTime.setText(str(self.cam_controller.cam.ExposureTime()))

    def update_plot(self):
        self.section_xcoord = np.arange(0, self.cam_controller.frame.shape[1])
        self.section_xdata = self.cam_controller.frame[self.section_yctr,::]
        self.sectionx_line.setData(self.section_xcoord, self.section_xdata)
        self.section_ycoord = np.arange(0, self.cam_controller.frame.shape[0])
        self.section_ydata = self.cam_controller.frame[::,self.section_xctr]
        self.sectiony_line.setData(self.section_ydata,self.section_ycoord)

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

    def label_mousepress(self):
        def mousepress(eventQMouseEvent):
            label_width = self.labelImage.size().width()
            label_height = self.labelImage.size().height()
            mouse_x = eventQMouseEvent.pos().x()
            mouse_y = eventQMouseEvent.pos().y()
            self.section_xctr = round(self.cam_controller.framewidth*mouse_x/label_width)
            self.section_yctr = round(self.cam_controller.frameheight*mouse_y/label_height)
            self.lineEditSectionX.setText(str(self.section_xctr))
            self.lineEditSectionY.setText(str(self.section_yctr))
        return mousepress

    def checkbox_auto_exposure(self):
        if self.checkBoxAutoExposure.isChecked():
            self.cam_controller.reset_exposure()
        else:
            self.set_exptime()

    def set_background(self):
        self.cam_controller.background = self.cam_controller.frame

    def clear_background(self):
        self.cam_controller.background = self.cam_controller.nobackground

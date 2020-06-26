import numpy as np
import PySpin
from PyQt5.QtCore import Qt, QThread, QTimer, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication, QGraphicsView, QLabel, QLineEdit, QGroupBox, QTextBrowser, QSizePolicy
from pyqtgraph import ImageView


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.horizontalLayoutWidget =QWidget(self.central_widget)
        # self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 931, 661))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QGraphicsView(self.horizontalLayoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.yplot = QLabel(self.horizontalLayoutWidget)
        self.yplot.setObjectName("yplot")
        self.gridLayout.addWidget(self.yplot, 0, 1, 1, 1)
        self.xplot = QLabel(self.horizontalLayoutWidget)
        self.xplot.setObjectName("xplot")
        self.gridLayout.addWidget(self.xplot, 1, 0, 1, 1)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QLabel(self.horizontalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_6 = QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.lineEdit_2 = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 0, 1, 1, 1)
        self.lineEdit_3 = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 1, 1, 1, 1)
        self.lineEdit_4 = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_2.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.lineEdit_5 = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_2.addWidget(self.lineEdit_5, 4, 1, 1, 1)
        self.lineEdit_6 = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_2.addWidget(self.lineEdit_6, 5, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(0, 3)
        self.gridLayout.setRowStretch(1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_8 = QLabel(self.horizontalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.lineEdit_7 = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_3.addWidget(self.lineEdit_7, 0, 1, 1, 1)
        self.label_7 = QLabel(self.horizontalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_9 = QLabel(self.horizontalLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)
        self.lineEdit_8 = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout_3.addWidget(self.lineEdit_8, 1, 1, 1, 1)
        self.lineEdit_9 = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout_3.addWidget(self.lineEdit_9, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.BoxLog = QGroupBox(self.horizontalLayoutWidget)
        self.BoxLog.setObjectName("BoxLog")
        self.textBrowser = QTextBrowser(self.BoxLog)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.BoxLog)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 1)


    def update_image(self):
        frame = self.cam.get_frame()
        self.image_view.setImage(frame)

    def update_movie(self):
        print('1')
        self.cam.acquire_continue()
        self.image_view.setImage(self.cam.frame)

    def update_brightness(self, value):
        value /= 10
        self.cam.set_brightness(value)

    def start_movie(self):
        # self.movie_thread = MovieThread(self.cam)
        # self.movie_thread.start()
        self.update_timer.start(100)


class MovieThread(QThread):
    def __init__(self, cam):
        super().__init__()
        self.cam = cam

    def run(self):
        self.cam.acquire_continue(1000)

if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())
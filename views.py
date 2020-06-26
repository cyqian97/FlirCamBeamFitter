import numpy as np
import PySpin
from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider
from pyqtgraph import ImageView


class StartWindow(QMainWindow):
    def __init__(self, camera = None):
        super().__init__()
        self.cam = camera

        self.central_widget = QWidget()
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)
        self.button_movie = QPushButton('Start Movie', self.central_widget)
        self.image_view = ImageView()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,10)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_frame)
        self.layout.addWidget(self.button_movie)
        self.layout.addWidget(self.image_view)
        self.layout.addWidget(self.slider)
        self.setCentralWidget(self.central_widget)

        self.button_frame.clicked.connect(self.update_image)
        self.button_movie.clicked.connect(self.start_movie)
        self.slider.valueChanged.connect(self.update_brightness)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)

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
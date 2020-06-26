from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.button_min = QPushButton('Get Minimum', self.central_widget)
        self.button_max = QPushButton('Get Maximum', self.central_widget)
        self.button_max.clicked.connect(self.button_clicked)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_min)
        self.layout.addWidget(self.button_max)
        self.setCentralWidget(self.central_widget)

    def button_clicked(self):
        print('Button Clicked')



if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())
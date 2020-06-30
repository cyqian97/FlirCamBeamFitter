Python
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.Qt import Qt

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 QGraphicView"
        self.top = 200
        self.left = 500
        self.width = 600
        self.height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGraphicView()

        self.show()

    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)

        self.pen = QPen(Qt.red)

        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0, 0, 600, 500)

        self.shapes()

    def shapes(self):
        ellipse = self.scene.addEllipse(20, 20, 200, 200, self.pen, self.greenBrush)
        rect = self.scene.addRect(-100, -100, 200, 200, self.pen, self.grayBrush)

        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        ellipse.setFlag(QGraphicsItem.ItemIsSelectable)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.Qt import Qt

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 QGraphicView"
        self.top = 200
        self.left = 500
        self.width = 600
        self.height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGraphicView()

        self.show()

    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)

        self.pen = QPen(Qt.red)

        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0, 0, 600, 500)

        self.shapes()

    def shapes(self):
        ellipse = self.scene.addEllipse(20, 20, 200, 200, self.pen, self.greenBrush)
        rect = self.scene.addRect(-100, -100, 200, 200, self.pen, self.grayBrush)

        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        ellipse.setFlag(QGraphicsItem.ItemIsSelectable)
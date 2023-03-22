import numpy as np
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QWidget, QFrame, QGroupBox, QHBoxLayout, QVBoxLayout
import cv2 as cv
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
from Release.biggusFolder.tools.sliderBox import sliderBox


# toDo: https://docs.opencv.org/4.x/d3/dbe/tutorial_opening_closing_hats.html
class toolz(QWidget):
    sld1: sliderBox
    sld2: sliderBox
    frame: QFrame
    grpBox: QGroupBox
    grpBoxLayout: QVBoxLayout
    layout: QHBoxLayout
    width: int = 300
    height: int = 200

    radiusChange = pyqtSignal(str)
    sigmaChange = pyqtSignal(str)
    valueChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.sld1 = sliderBox("radius")
        self.sld1.setSliderRange(0, 100)
        self.sld2 = sliderBox("sigma")
        self.sld2.setSliderRange(0, 100)
        self.initUI()
        self.initConnections()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.frame = QFrame(flags=Qt.WindowFlags())
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setContentsMargins(5, 5, 5, 5)
        self.frame.setFixedSize(self.width, self.height)
        self.frame.setLayout(QVBoxLayout())
        # aggiunge una groupBox
        self.grpBox = QGroupBox("Blur Tool")
        self.grpBox.setFixedSize(self.width - 10, self.height - 10)
        self.grpBoxLayout = QVBoxLayout()
        self.grpBox.setLayout(self.grpBoxLayout)
        self.grpBoxLayout.addWidget(self.sld1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grpBoxLayout.addWidget(self.sld2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.frame.layout().addWidget(self.grpBox)
        mainLayout.addWidget(self.frame)
        self.setLayout(mainLayout)

    def initConnections(self):
        self.sld1.valueChanged.connect(self.onRadiusChange)
        self.sld2.valueChanged.connect(self.onSigmaChange)
        self.sld1.valueChanged.connect(self.valueChanged)
        self.sld2.valueChanged.connect(self.valueChanged)

    def onRadiusChange(self, value):
        self.radiusChange.emit(str(value))

    def onSigmaChange(self, value):
        self.sigmaChange.emit(str(value))

class ErodeMorphCvNode(AbstractNodeInterface):
    startValue = ""
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242), QColor(255, 91, 110), QColor(142, 255, 242), QColor(218, 255, 251),
                  QColor(110, 255, 91), QColor(170, 61, 73), QColor(52, 19, 23), QColor(142, 255, 242), ]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"
    menuReturnValue = "open"
    radius = 0
    sigma = 0
    toolBox: toolz

    def __init__(self, value=None, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("ErodeMorph")
        self.setName("ErodeMorph")
        self.nodeGraphic.drawStripes = True
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        operations = {
            "open": self.doOpen,
            "close": self.doClose,
            "gradient": self.doGradient,
            "topHat": self.doTopHat,
            "blackHat": self.doBlackHat
        }
        value = operations[self.menuReturnValue]()

        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("change name of menu here")
        action1 = contextMenu.addAction("open")
        action2 = contextMenu.addAction("close")
        action3 = contextMenu.addAction("gradient")
        action4 = contextMenu.addAction("topHat")
        action5 = contextMenu.addAction("blackHat")

        action = contextMenu.exec(position)
        self.menuReturnValue = action.text()
        if action == action1:
            self.doOpen()
        elif action == action2:
            self.doClose()
        elif action == action3:
            self.doGradient()
        elif action == action4:
            self.doTopHat()
        elif action == action5:
            self.doBlackHat()

        self.updateAll()
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def doOpen(self):
        img1 = self.inPlugs[0].getValue()
        kernel = np.ones((5, 5), np.uint8)
        return cv.morphologyEx(img1, cv.MORPH_OPEN, kernel)

    def doClose(self):
        img1 = self.inPlugs[0].getValue()
        kernel = np.ones((5, 5), np.uint8)
        return cv.morphologyEx(img1, cv.MORPH_CLOSE, kernel)

    def doGradient(self):
        img1 = self.inPlugs[0].getValue()
        kernel = np.ones((5, 5), np.uint8)
        return cv.morphologyEx(img1, cv.MORPH_GRADIENT, kernel)

    def doTopHat(self):
        img1 = self.inPlugs[0].getValue()
        kernel = np.ones((5, 5), np.uint8)
        return cv.morphologyEx(img1, cv.MORPH_TOPHAT, kernel)

    def doBlackHat(self):
        img1 = self.inPlugs[0].getValue()
        kernel = np.ones((5, 5), np.uint8)
        return cv.morphologyEx(img1, cv.MORPH_BLACKHAT, kernel)

    def onRadiusChange(self, value):
        value = int(value)
        if value % 2 == 0:
            value += 1
        self.radius = value
        self.calculateOutput(0)
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()

    def onSigmaChange(self, value):
        value = int(value)

        self.sigma = value
        self.calculateOutput(0)
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
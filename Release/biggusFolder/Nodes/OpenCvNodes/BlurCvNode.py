import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2 as cv
import sys
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
from BiggusMain.elements.tools.blurTool import blurTool


class cmbBoxWidget(QWidget):
    layout: QHBoxLayout
    combo: QComboBox
    style = f"""
        font: 6pt "Segoe UI";
        background-color: transparent;
        color: rgb(240, 240, 255);
        """
    radiusChange = pyqtSignal(int, name="radiusChange")
    sigmaChange = pyqtSignal(int, name="sigmaChange")

    def __init__(self, reference, parent=None):
        super().__init__(parent)
        self.toolBox = blurTool()
        self.reference = reference
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.combo = QComboBox(self)
        self.combo.addItems(["Gaussian", "Median", "Box", "Bilateral"])
        self.layout.addWidget(self.combo, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(self.style)

    def initConnections(self):
        self.combo.currentIndexChanged.connect(self.onComboChanged)

    def onComboChanged(self, index):
        self.toolBox.setRange(0, 80)
        if index == 0 or index not in [1, 2]:
            self.toolBox.setRadius(5)
            self.toolBox.setSigma(0)
        elif index == 1:
            self.toolBox.setRadius(7)
            self.toolBox.setSigma(0)
        elif index == 2:
            self.toolBox.setRadius(9)
            self.toolBox.setSigma(75)

    def showToolBox(self, pos):
        self.toolBox.setGeometry(int(pos.x()), int(pos.y()), 300, 100)
        self.toolBox.show()


class BlurCvNode(AbstractNodeInterface):
    startValue = ""
    width = 180
    height = 120
    colorTrain = [QColor(255, 234, 242), QColor(255, 91, 110), QColor(142, 255, 242), QColor(218, 255, 251),
                  QColor(110, 255, 91), QColor(170, 61, 73), QColor(52, 19, 23), QColor(142, 255, 242), ]
    radius = 7
    sigma = 0
    lastValue = None
    proxyWidget: cmbBoxWidget
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value=20, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("BlurCvNode")
        self.setName("BlurCvNode")
        self.nodeGraphic.drawStripes = True
        self.changeSize(self.width, self.height)
        self.AddProxyWidget()

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        if value is not None:
            operation = {
                "Gaussian": self.doGaussian,
                "Median": self.doMedian,
                "Box": self.doBox,
                "Filter2D": self.doFilter2D,
                "Bilateral": self.doBilateral,
            }
            self.outPlugs[plugIndex].setValue(operation[self.proxyWidget.combo.currentText()](value))

        else:
            print("no image")
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def doGaussian(self, image):
        return cv2.GaussianBlur(image, (self.radius, self.radius), self.sigma)

    def doMedian(self, image):
        return cv2.medianBlur(image, self.radius)

    def doBox(self, image):
        """
        cv2. boxfilter(src, dst, ddepth, ksize, anchor, normalize, bordertype)

        src - It denotes the source of the image. It can be an 8-bit or floating-point, 1-channel image.
        dst- It denotes the destination image of the same size. Its type will be the same as the src image.
        ddepth - It denotes the output image depth.
        ksize - It blurs the kernel size.
        anchor - It denotes the anchor points. By default, its value Point to coordinates (-1,1), which means that the anchor is at kernel center.
        normalize - It is the flag, specifying whether the kernel should be normalized or not.
        borderType - An integer object represents the type of the border used.

        :param image:
        :return:
        """
        return cv2.boxFilter(image, -1, (self.radius, self.radius))

    def doFilter2D(self, image):
        """
        cv2.filter2D(src, ddepth, kernel, dst, anchor, delta, borderType)

        src - It denotes the source of the image. It can be an 8-bit or floating-point, 1-channel image.
        dst- It denotes the destination image of the same size. Its type will be the same as the src image.
        ddepth - It denotes the output image depth.
        kernel - It is the kernel matrix.
        anchor - It denotes the anchor points. By default, its value Point to coordinates (-1,1), which means that the anchor is at kernel center.
        delta - It is the added value to the filtered pixels.
        borderType - An integer object represents the type of the border used.

        :param image:
        :return:
        """
        return cv2.filter2D(image, -1, (self.radius, self.radius))

    def doBilateral(self, image):
        return cv2.bilateralFilter(image, self.radius, self.sigma, self.sigma)

    def doErode(self, image):
        return cv2.erode(image, (self.radius, self.radius))

    def AddProxyWidget(self):
        self.proxyWidget = cmbBoxWidget(self)
        self.proxyWidget.setFixedWidth(self.width - 20)

        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height - self.proxyWidget.height()))
        self.setDefaultParameters()
        self.proxyWidget.toolBox.radiusChanged.connect(self.onRadiusChange)
        self.proxyWidget.toolBox.sigmaChanged.connect(self.onSigmaChange)
        self.proxyWidget.toolBox.valueChanged.connect(self.nodeData.calculate)

    def setDefaultParameters(self):
        self.proxyWidget.combo.setCurrentIndex(0)
        self.proxyWidget.toolBox.setRadius(7)
        self.proxyWidget.toolBox.setSigma(0)

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

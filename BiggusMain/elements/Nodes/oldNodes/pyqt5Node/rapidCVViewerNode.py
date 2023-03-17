import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
import cv2


class ImageViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._image = None

    def setImage(self, image):
        self._image = image
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self._image is not None:
            # deve mantenere l'aspectRatio dell'immagine
            imageAspectRatio = self._image.width() / self._image.height()
            widgetAspectRatio = self.width() / self.height()
            if imageAspectRatio > widgetAspectRatio:
                scaledHeight = self.width() / imageAspectRatio
                scaledWidth = self.width()
            else:
                scaledHeight = self.height()
                scaledWidth = self.height() * imageAspectRatio
            scaledImage = self._image.scaled(int(scaledWidth), int(scaledHeight), Qt.AspectRatioMode.KeepAspectRatio)
            painter.drawImage(QRectF(0, 0, self.width(), self.height()), scaledImage)


class rapidCVViewerNode(AbstractNodeInterface):
    startValue = 0
    width = 640 - 200
    height = 480 - 200
    colorTrain = [QColor(28, 134, 26), QColor(230, 255, 249), QColor(23, 255, 102), QColor(63, 255, 128),
                  QColor(123, 255, 168), QColor(11, 167, 64), QColor(0, 0, 0), QColor(23, 255, 102)]
    menuReturnValue = "normal"
    proxyWidget: ImageViewerWidget
    logo = r"Release/biggusFolder/imgs/logos/Qt.png"

    def __init__(self, value=None, inNum=1, outNum=1, parent=None):
        super().__init__("ImageViewerNode", inNum, outNum, parent)
        self.setClassName("rapidCVViewerNode")
        self.setName("rapidViewer")
        self.AddProxyWidget()
        self.nodeGraphic.drawStripes = True
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        image = self.inPlugs[0].getValue()
        operations = {
            "normal": self.doNormal,
            "blueCheck": self.doBlueCheck,
        }
        value = operations[self.menuReturnValue](image)
        if isinstance(value, np.ndarray):
            self.proxyWidget.setImage(value)
            if len(value.shape) == 2:
                value = cv2.cvtColor(value, cv2.COLOR_GRAY2BGR)  # converti l'immagine in scala di grigio in BGR
            elif len(value.shape) == 3 and value.shape[2] == 4:
                value = cv2.cvtColor(value, cv2.COLOR_RGBA2BGR)  # converti l'immagine RGBA in BGR
            elif len(value.shape) == 3 and value.shape[2] == 2:
                value = cv2.cvtColor(value, cv2.COLOR_GRAY2BGR)  # converti l'immagine a 2 canali in BGR
            height, width, channel = value.shape
            bytesPerLine = 3 * width
            qImg = QImage(value.data, width, height, bytesPerLine,
                          QImage.Format.Format_BGR888)  # converte l'immagine in un oggetto QImage in formato BGR
            self.proxyWidget.setImage(qImg)
        elif isinstance(value, QImage):
            self.proxyWidget.setImage(value)
        self.updateAll()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def showContextMenu(self, position):
        menu = QMenu()
        _normal = menu.addAction("Normal")
        _blueCheck = menu.addAction("blueCheck")

        action = menu.exec_(position)
        if action is not None:
            self.menuReturnValue = action.text()
        if action == _normal:
            image = self.inPlugs[0].getValue()
            self.menuReturnValue = "normal"
            self.outPlugs[0].setValue(self.doNormal(image))
        elif action == _blueCheck:
            image = self.inPlugs[0].getValue()
            self.menuReturnValue = "blueCheck"
            self.outPlugs[0].setValue(self.doBlueCheck(image))

        self.updateAll()
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def doNormal(self, image):
        return image

    def doBlueCheck(self, image):
        if isinstance(image, np.ndarray):
            blue_channel_only = np.zeros(image.shape, dtype=np.uint8)
            blue_channel_only[:, :, 0] = image[:, :, 0]  # Usa il canale blu invece del rosso

            # Annulla il canale rosso e verde nelle aree appropriate
            mask = np.zeros(image.shape[:2], dtype=bool)  # Utilizza bool invece di np.bool
            for i in range(1, 7, 2):
                mask[:, int(i * image.shape[1] / 7):int((i + 1) * image.shape[1] / 7)] = True
            blue_channel_only[mask, 1] = 0
            blue_channel_only[mask, 2] = 0  # Annulla il canale rosso invece del blu

            return blue_channel_only

    def setImage(self, image):
        self.viewer.setImage(image)

    def AddProxyWidget(self):
        self.viewer = ImageViewerWidget()
        self.proxyWidget = self.viewer
        self.proxyWidget.setFixedSize(self.width - 20, self.height - 50)
        self.nodeGraphic.createProxyWidget(self.proxyWidget)
        self.proxyWidget.setFixedWidth(self.width - 20)
        self.proxyWidget.setFixedHeight(self.height - 50)
        self.proxyWidget.move(int(self.width // 2 - self.proxyWidget.width() // 2),
                              int(self.height // 2 - self.proxyWidget.height() // 2) + 20)

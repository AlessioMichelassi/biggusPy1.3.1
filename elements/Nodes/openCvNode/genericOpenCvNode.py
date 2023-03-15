from PyQt5.QtCore import QDir
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu, QFileDialog
import cv2 as cv
import sys
from elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class CvNode(AbstractNodeInterface):
    startValue = ""
    width = 80
    height = 120
    colorTrain = [QColor(255, 234, 242),QColor(255, 91, 110),QColor(142, 255, 242),QColor(218, 255, 251),QColor(110, 255, 91),QColor(170, 61, 73),QColor(52, 19, 23),QColor(142, 255, 242),]
    logo = r"Release/biggusFolder/imgs/logos/openCvLogo.png"

    def __init__(self, value= 20, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("CvNode")
        self.setName("CvNode")
        self.nodeGraphic.drawStripes = True
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        path = self.inPlugs[0].getValue()
        value = cv.imread(path)
        if value is None:
            value = cv.imread(self.startValue)
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("change name of menu here")
        action1 = contextMenu.addAction("action1")
        action2 = contextMenu.addAction("action2")
        action3 = contextMenu.addAction("action3")

        action = contextMenu.exec(position)
        if action == action1:
            self.doAction1()
        elif action == action2:
            self.doAction2()
        elif action == action3:
            self.doAction3()

    def doAction1(self):
        pass

    def doAction2(self):
        pass

    def doAction3(self):
        pass

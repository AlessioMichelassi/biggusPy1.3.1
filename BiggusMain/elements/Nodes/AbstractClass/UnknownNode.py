from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class UnknownNode(AbstractNodeInterface):
    startValue = 0
    width = 50
    height = 120
    colorTrain = [QColor(13, 9, 9), QColor(240, 0, 4), QColor(9, 13, 11), QColor(71, 38, 225), QColor(245, 191, 58),
                  QColor(21, 0, 0), QColor(226, 0, 4), QColor(210, 253, 163), ]

    def __init__(self, value=0, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("UnknownNode")
        self.setName("UnknownNode")
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def redesign(self):
        self.changeSize(self.width, self.height)
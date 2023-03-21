# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class NumberNode(AbstractNodeInterface):

    startValue = 0
    width = 50
    height = 120
    colorTrain = [QColor(177, 225, 40), QColor(95, 217, 173), QColor(143, 129, 158), QColor(91, 240, 171),
                  QColor(220, 215, 146), QColor(30, 31, 2), QColor(97, 239, 255), QColor(149, 97, 228), ]
    menuReturnValue = "int"

    def __init__(self, value=80, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("NumberNode")
        self.setName("NumberNode")
        self.changeSize(self.width, self.height)
        self.changeInputValue(0, value, True)

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        if not isinstance(value, (int, float)):
            value = self.changeType(int)
            self.changeInputValue(0, value, True)
        else:
            value = self.inPlugs[0].getValue()
        self.outPlugs[plugIndex].setValue(value)
        return self.outPlugs[plugIndex].getValue()

    def getCode(self):
        if not self.inConnections:
            return f'{self.getTitle()} = {self.inPlugs[0].getValue()}'
        inPlugNodeName, code = self.getCodeFromInput(0)
        return (
            f'{self.getTitle()} = {self.inPlugs[0].getValue()}'
            if inPlugNodeName is None
            else f'{code}\n{self.getTitle()} = int({inPlugNodeName})')

    def redesign(self):
        self.changeSize(self.width, self.height)

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("set biggusNode")
        actionInt = contextMenu.addAction("int")
        actionFloat = contextMenu.addAction("float")
        actionRandomInt = contextMenu.addAction("random int")
        actionRandomFloat = contextMenu.addAction("random float")
        actionPI = contextMenu.addAction("pi")
        actionEuler = contextMenu.addAction("euler")

        action = contextMenu.exec(position)
        if action == actionInt:
            self.changeInputValue(0, self.changeType(int), True)
        elif action == actionFloat:
            self.changeInputValue(0, self.changeType(float), True)
        elif action == actionRandomInt:
            self.randomInt()
        elif action == actionRandomFloat:
            self.randomFloat()
        elif action == actionPI:
            self.pi()
        elif action == actionEuler:
            self.euler()
        elif action == "reset":
            self.changeInputValue(0, self.startValue, True)

        if action is not None:
            self.menuReturnValue = action.text()
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def changeType(self, _type):
        try:
            value = _type(self.inPlugs[0].getValue())
        except ValueError:
            print(f"WARNING: you are trying to cast a {type(self.inPlugs[0].getValue())} to {_type.__name__} but it "
                  f"is not possible")
            value = 0
        return value

    def randomInt(self):
        value = random.randint(1, 99)
        self.changeInputValue(0, value, True)
        self.updateAll()
        return value

    def randomFloat(self):
        value = random.uniform(1.0, 99.0)
        self.changeInputValue(0, value, True)
        self.updateAll()
        return value

    def pi(self):
        value = math.pi
        self.changeInputValue(0, value, True)
        self.updateAll()
        return value

    def euler(self):
        value = math.e
        self.changeInputValue(0, value, True)
        self.updateAll()
        return value

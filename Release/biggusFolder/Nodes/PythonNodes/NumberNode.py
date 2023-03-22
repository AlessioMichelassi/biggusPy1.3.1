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
    contextMenu = None

    def __init__(self, value=80, inNum=1, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("NumberNode")
        self.setName("NumberNode")
        self.changeSize(self.width, self.height)
        self.checkInputForType(value)

    def checkInputForType(self, value):
        if isinstance(value, int):
            self.changeInputValue(0, int(value), True)
        elif isinstance(value, float):
            self.changeInputValue(0, float(value), True)
        elif isinstance(value, str):
            floatString = value.replace(",", ".")
            if floatString.isnumeric():
                self.changeInputValue(0, int(floatString), True)
            elif floatString.replace(".", "").isnumeric():
                self.changeInputValue(0, float(floatString), True)
        else:
            print(f"NumberNode: wrong input type: {value} is of type {type(value)}")

    def calculateOutput(self, plugIndex):
        value = self.inPlugs[0].getValue()
        if not isinstance(value, (int, float)):
            value = self.changeType()
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
        self.contextMenu = QMenu()
        self.contextMenu.addSection("set biggusNode")
        actionInt = self.contextMenu.addAction("int")
        actionFloat = self.contextMenu.addAction("float")
        actionRandomInt = self.contextMenu.addAction("random int")
        actionRandomFloat = self.contextMenu.addAction("random float")
        actionPI = self.contextMenu.addAction("pi")
        actionEuler = self.contextMenu.addAction("euler")

        action = self.contextMenu.exec(position)
        if action == actionInt:
            self.menuReturnValue = "int"
            self.changeInputValue(0, self.changeType(), True)
        elif action == actionFloat:
            self.menuReturnValue = "float"
            self.changeInputValue(0, self.changeType(), True)
        elif action == actionRandomInt:
            self.menuReturnValue = "int"
            self.randomInt()
        elif action == actionRandomFloat:
            self.menuReturnValue = "float"
            self.randomFloat()
        elif action == actionPI:
            self.menuReturnValue = "float"
            self.pi()
        elif action == actionEuler:
            self.menuReturnValue = "float"
            self.euler()
        elif action == "reset":
            self.menuReturnValue = "int"
            self.changeInputValue(0, self.startValue, True)

        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def changeType(self):
        if "int" in self.menuReturnValue:
            value = self.inPlugs[0].getValue()
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    print(f"WARNING: the value {value} cannot be converted to an integer")
                    value = 0
            else:
                value = int(value)
        else:
            value = self.inPlugs[0].getValue()
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    print(f"WARNING: the value {value} cannot be converted to a float")
                    value = 0.0
            else:
                value = float(value)
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

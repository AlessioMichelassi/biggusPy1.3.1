# -*- coding: utf-8 -*-
import math
import random

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMenu

from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface


class MathNode(AbstractNodeInterface):
    startValue = 0
    menuReturnValue = "sum"
    width = 120
    height = 80
    colorTrain = [QColor(148, 209, 178), QColor(92, 10, 50), QColor(250, 47, 200), QColor(117, 66, 246),
                  QColor(85, 230, 143), QColor(11, 39, 149), QColor(176, 103, 92), QColor(84, 255, 4)]

    def __init__(self, value=1, inNum=2, outNum=1, parent=None):
        super().__init__(value, inNum, outNum, parent)
        self.setClassName("MathNode")
        self.setName("SumNode")
        self.changeSize(self.width, self.height)

    def calculateOutput(self, plugIndex):
        if self.nodeData.checkInput(int):
            val1 = self.inPlugs[0].getValue()
            val2 = self.inPlugs[1].getValue()
            if val2 == 0:
                val2 = 1
            operations = {
                "sum": val1 + val2,
                "subtraction": val1 - val2,
                "division": val1 / val2,
                "divisionInt": val1 // val2,
                "module": val1 % val2,
                "multiplication": val1 * val2,
                "exponentiation": val1 ** val2,
            }
            value = operations[self.menuReturnValue]
            self.outPlugs[plugIndex].setValue(value)
            self.nodeGraphic.updateTxtValuePosition()
            return self.outPlugs[plugIndex].getValue()
        else:
            print("Error in input")

    def getCode(self):
        return self.returnMathCode()

    def redesign(self):
        self.changeSize(self.width, self.height)
        self.nodeGraphic.setTxtValueReadOnly(True)
        self.updateAll()

    def showContextMenu(self, position):
        contextMenu = QMenu()
        contextMenu.addSection("operation")
        actionPlus = contextMenu.addAction("sum")
        actionMinus = contextMenu.addAction("subtraction")
        actionDiv = contextMenu.addAction("division")
        actionDivInt = contextMenu.addAction("divisionInt")
        actionModule = contextMenu.addAction("module")
        actionMult = contextMenu.addAction("multiplication")
        actionExp = contextMenu.addAction("exponentiation")
        action = contextMenu.exec(position)
        self.menuReturnValue = action.text()
        if action == actionPlus:
            self.execMenu(actionPlus, "Sum")
        elif action == actionMinus:
            self.execMenu(actionMinus, "Subtraction")
        elif action == actionDiv:
            self.execMenu(actionDiv, "Division")
        elif action == actionDivInt:
            self.execMenu(actionDivInt, "DivisionInt")
        elif action == actionModule:
            self.execMenu(actionModule, "Module")
        elif action == actionMult:
            self.execMenu(actionMult, "Multiplication")
        elif action == actionExp:
            self.execMenu(actionExp, "Exponentiation")

    def execMenu(self, arg0, arg1):
        self.menuReturnValue = arg0.text()
        title = arg1
        self.setGraphicTitleText(title)
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def updateNode(self, className, value):
        title = className.title()
        self.nodeGraphic.setTitle(title)
        self.setGraphicTitleText(title)
        self.updateInPlugValueFromGraphics(value)

    def setOperator(self, operator):
        self.menuReturnValue = operator
        title = operator
        self.setGraphicTitleText(title)
        if self.nodeData.outConnections:
            for connection in self.nodeData.outConnections:
                connection.updateValue()
        else:
            self.nodeData.calculate()

    def returnMathCode(self):
        val1Title, val1Code = self.getCodeFromInput(0)
        val2Title, val2Code = self.getCodeFromInput(1)
        concatCode = f"{val1Code}\n{val2Code}"
        return f"{concatCode}\n{self.getTitle()} = {val1Title} {self.menuReturnValue} {val2Title}"
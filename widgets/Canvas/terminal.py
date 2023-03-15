import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from scratchNodeV0_9.ArguePy_CodeEditor.editorWidgetTool.tools.codeEditor import pythonCodeEditor
from widgets.Canvas.nodeCodeInterpreter import NodeCodeInterpreter


class Terminal(pythonCodeEditor):
    backgroundColor: QColor = QColor(30, 31, 34)
    textColor: QColor = QColor(167, 183, 198)
    lineNumberColor: QColor = QColor(200, 200, 240, 255)
    lineNumberBackgroundColor: QColor = backgroundColor.darker(110)
    indentationLineColor: QColor = QColor(255, 100, 100, 255)
    systemFont: QFont = QFont("Lohit Gujarati", 8)
    terminalSignal = pyqtSignal(str)
    messageSignal = pyqtSignal(str)
    nodeCodeInterpreter: NodeCodeInterpreter

    def __init__(self, biggusPy, parent=None):
        super().__init__(parent)
        self.biggusPy = biggusPy
        self.nodeCodeInterpreter = NodeCodeInterpreter(self.biggusPy, self.biggusPy.canvas)

    def updateSystemColors(self):
        # dovrebbe cambiare solo lo sfondo non tutto il colore del widget
        style = f"QPlainTextEdit {{background-color: {self.backgroundColor.name()}; color: {self.textColor.name()};}}"
        self.setStyleSheet(style)

    def keyPressEvent(self, event):
        # se viene premuto CTRL + RETURN
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key.Key_Return:
            # prende l'ultima riga e la passa al nodeCodeInterpreter
            command = self.toPlainText().splitlines()
            for com in command:
                self.nodeCodeInterpreter.parseCommand(com)
            # self.insertPlainText(f"{self.prompt}\n ")
            self.clear()
            return
        super().keyPressEvent(event)

    def handleCommand(self, command):
        self.terminalSignal.emit(command)

    def printMessage(self, message):
        self.insertPlainText(message)
        self.messageSignal.emit(message)

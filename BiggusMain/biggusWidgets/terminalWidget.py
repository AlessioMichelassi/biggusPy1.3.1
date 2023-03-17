import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.biggusWidgets.customFocusWidget import customFocusWidget
from scratchONodeV0_9.ArguePy_CodeEditor.editorWidgetTool.tools.codeEditor import pythonCodeEditor


class Terminal(customFocusWidget):
    argue: pythonCodeEditor
    terminalSignal = pyqtSignal(str)
    messageSignal = pyqtSignal(str)

    def __init__(self, biggusPy, canvas, parent=None):
        super().__init__(parent)
        self.biggusPy = biggusPy
        self.canvas = canvas
        layout = QVBoxLayout()
        self.argue = pythonCodeEditor(self.biggusPy, self.canvas)
        layout.addWidget(self.argue, 1, Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        # Sovrascrivi il menu contestuale di pythonCodeEditor
        self.argue.setContextMenuPolicy(Qt.CustomContextMenu)
        self.argue.customContextMenuRequested.connect(self.createContextMenu)

    def updateSystemColors(self):
        # dovrebbe cambiare solo lo sfondo non tutto il colore del widget
        style = f"QPlainTextEdit {{background-color: {self.backgroundColor.name()}; color: {self.textColor.name()};}}"
        self.setStyleSheet(style)

    def createContextMenu(self, pos) -> None:
        # deve ignorare il precedente menu
        menu = QMenu(self)
        actionClear = menu.addAction("Clear")
        separator = menu.addSeparator()
        actionSend = menu.addAction("Send")
        action = menu.exec_(self.argue.mapToGlobal(pos))
        if action == actionSend:
            self.sendToCanvas()
        elif action == actionClear:
            self.clear()

    def contextMenuEvent(self, event) -> None:
        # Non fare nulla qui, il menu contestuale verrà gestito nella funzione createContextMenu()
        pass

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Tab:
            self.argue.keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def sendToCanvas(self):
        command = self.toPlainText().splitlines()
        for com in command:
            self.nodeCodeInterpreter.parseCommand(com)
        self.clear()

    def handleCommand(self, command):
        self.terminalSignal.emit(command)

    def printMessage(self, message):
        self.argue.insertPlainText(message)
        self.messageSignal.emit(message)

    def clean(self):
        self.argue.clear()

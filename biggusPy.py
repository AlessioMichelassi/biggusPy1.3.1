import json
import pprint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from widgets.Canvas.Canvas import Canvas
from widgets.Canvas.nodeBrowser import NodeBrowser
from widgets.Canvas.nodeCodeInterpreter import NodeCodeInterpreter
from widgets.Canvas.terminal import Terminal

from widgets.Menu.biggusMenu import BiggusMenu


class biggusPy(QMainWindow):

    canvas: Canvas
    nodeBrowser: NodeBrowser
    terminal: Terminal
    nodeCodeInterpreter: NodeCodeInterpreter
    statusMousePosition: QLabel
    path = "saveDir"
    fileName = "untitled"
    recentFilesMenu: BiggusMenu
    recentFiles = []
    pythonFolderPath = r"elements/Nodes/PythonNodes"

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowFlags())
        self.setGeometry(100, 100, 1440, 900)
        self.setWindowTitle("BiggusPy(a great Caesar's friend) V0.1.3")
        self.setWindowIcon(QIcon('elements/imgs/BiggusIcon.ico'))
        self.initUI()

    def initUI(self):
        self.canvas = Canvas()
        split2 = QSplitter(Qt.Orientation.Horizontal)
        self.nodeBrowser = NodeBrowser(self.canvas)
        self.terminal = Terminal(self)
        grpBox = QGroupBox("Terminal")
        grpBox.setFont(QFont("Lucida Console", 8))
        grpBox.setContentsMargins(0, 20, 10, 5)
        grpBox.setStyleSheet("QGroupBox {border: 0px solid gray; border-radius: 9px; margin-top: 0.5em;}")
        grpBoxLayout = QVBoxLayout()
        grpBoxLayout.addWidget(self.terminal)
        grpBox.setLayout(grpBoxLayout)

        self.nodeCodeInterpreter = NodeCodeInterpreter(self, self.canvas)
        split2.addWidget(self.nodeBrowser)
        split2.addWidget(grpBox)

        split1 = QSplitter(Qt.Orientation.Vertical)
        split1.addWidget(self.canvas)
        split1.addWidget(split2)
        self.setCentralWidget(split1)
        menu = BiggusMenu(self)
        self.setMenuBar(menu)
        self.createStatusBar()

    def initSize(self):
        self.nodeBrowser.setMaximumHeight((self.height() // 3))
        self.nodeBrowser.setMinimumHeight((self.height() // 3))

    def initConnections(self):
        self.canvas.graphicView.scenePosChanged.connect(self.onScenePosChanged)
        self.terminal.terminalSignal.connect(self.onTerminalInput)
        self.terminal.messageSignal.connect(self.onTerminalMessage)

    def restartCanvas(self):
        self.canvas.cleanTheScene()
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        self.statusMousePosition = QLabel("")
        self.statusBar().addPermanentWidget(self.statusMousePosition)
        self.canvas.graphicView.scenePosChanged.connect(self.onScenePosChanged)

    def onScenePosChanged(self, x, y):
        self.statusMousePosition.setText(f"Scene Pos: {x}:{y}")

    def saveFile(self, filename, fileData):
        with open(filename, "w+") as file:
            file.write(fileData)

    def readDataJason(self, file):
        canvas = json.loads(file)
        print(f"canvasName: {canvas['name']}")
        print(f"width: {canvas['sceneWidth']}")
        print(f"height: {canvas['sceneHeight']}")
        print(f"Nodes:\n")
        nodes = canvas['Nodes']
        for node in nodes:
            ppj = pprint.pformat(node).replace("'", '')
            print(ppj)

    # ################################################
    #
    #               KEYBOARD EVENTS
    #

    def event(self, event):
        # per intercettare il tasto tab c'è bisogno che venga controllato
        # prima di ogni evento
        if event.type() == QEvent.Type.KeyPress:
            if not self.canvas.graphicView.isTabWindowsOpen:
                if event.key() == Qt.Key.Key_Tab:
                    self.canvas.graphicView.openTabWindow()
                    return True
        return super().event(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.checkKeyFor(event)
        super().keyPressEvent(event)

    def checkKeyFor(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.canvas.graphicView.deleteSelectedItems()
        elif event.key() == Qt.Key.Key_D:
            self.canvas.graphicView.disableNode()
        elif event.key() == Qt.Key.Key_C:
            if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
                self.canvas.graphicView.copyNode()
        elif event.key() == Qt.Key.Key_V:
            if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
                self.canvas.pasteNode()
        else:
            return super().keyPressEvent(event)

    # ------------------ SHOW ON CANVAS ------------------

    def printOnStatusBar(self, text):
        self.statusBar().showMessage(text, 2000)

    def onTerminalInput(self, command):
        print(f"command: {command}")
        self.nodeCodeInterpreter.parseCommand(command)

    def onTerminalMessage(self, message):
        self.terminal.insertPlainText(message)

    def sendToTerminal(self, message):
        self.terminal.insertPlainText(message)
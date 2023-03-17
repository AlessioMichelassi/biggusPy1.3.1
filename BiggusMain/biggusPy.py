import json
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.Menu.biggusMenu import BiggusMenu
from BiggusMain.biggusWidgets.canvas import Canvas
from BiggusMain.biggusWidgets.customFocusWidget import customFocusWidget
from BiggusMain.biggusWidgets.nodeBrowserWidget import NodeBrowser
from BiggusMain.biggusWidgets.terminalWidget import Terminal


class BiggusPy(QMainWindow):
    canvas: Canvas
    nodeBrowser: NodeBrowser
    terminal: Terminal

    statusMousePosition: QLabel
    path = "saveDir"
    fileName = "untitled"
    recentFilesMenu: BiggusMenu
    recentFiles = []
    pythonFolderPath = {"python": "Release/biggusFolder/Nodes/PythonNodes",
                        "pyQt5": "Release/biggusFolder/Nodes/PyQt5Nodes",
                        "openCv": "Release/biggusFolder/Nodes/OpenCvNodes"}
    iconPaths = {"biggusIcon": "Release/biggusFolder/imgs/icon/biggusIcon",
                 "pythonIcon": "Release/biggusFolder/imgs/icon/pythonIcon"}

    logoPaths = {"pythonLogo": "Release/biggusFolder/imgs/logo/pythonLogo",
                 "pyQt5Logo": "Release/biggusFolder/imgs/logo/pyQt5Logo",
                 "openCvLogo": "Release/biggusFolder/imgs/logo/openCvLogo"}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1440, 900)
        self.setWindowTitle("BiggusPy(a great Caesar's friend) V0.1.3.1")
        self.setWindowIcon(QIcon('elements/imgs/BiggusIcon.ico'))
        self.openConfigFile()
        self.initMainUI()
        self.initMenu()

    def initMainUI(self):
        # crea i widget
        self.canvas = Canvas()
        self.nodeBrowser = NodeBrowser(self, self.canvas)
        self.terminal = Terminal(self, self.canvas)

        mainSplit = QSplitter(Qt.Orientation.Vertical)
        mainSplit.addWidget(self.canvas)
        bottomSplit = QSplitter(Qt.Orientation.Horizontal)
        bottomSplit.addWidget(self.nodeBrowser)
        bottomSplit.addWidget(self.terminal)
        mainSplit.addWidget(bottomSplit)
        self.setCentralWidget(mainSplit)

    def initMenu(self):
        menu = BiggusMenu(self)
        self.setMenuBar(menu)
        self.createStatusBar()
        self.canvas.node_name_list = menu.availableNodes

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        self.statusMousePosition = QLabel("")
        self.statusBar().addPermanentWidget(self.statusMousePosition)
        self.canvas.graphicView.scenePosChanged.connect(self.onScenePosChanged)

    def onScenePosChanged(self, x, y):
        self.statusMousePosition.setText(f"Scene Pos: {x}:{y}")

    def restartCanvas(self):
        self.canvas.cleanTheScene()
        self.terminal.clean()

    def printOnStatusBar(self, text):
        self.statusBar().showMessage(text)

    def openConfigFile(self):
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
            self.iconPaths = data["iconPaths"]
            self.logoPaths = data["logoPaths"]
            self.pythonFolderPath = data["pythonFolderPath"]
        except FileNotFoundError:
            self.saveConfigFile()

    def saveConfigFile(self):
        data = {"iconPaths": self.iconPaths,
                "logoPaths": self.logoPaths,
                "pythonFolderPath": self.pythonFolderPath}

        with open("config.json", "w") as f:
            json.dump(data, f)

    def returnPath(self, key):
        path = self.pythonFolderPath[key]
        nodes_folder = os.path.abspath(path)
        relative_path = os.path.relpath(nodes_folder, os.getcwd())
        modulePath = f"{relative_path.replace('/', '.')}"
        return f"{relative_path}/"

    def returnIconPath(self, key):
        return self.iconPaths[key]

    def returnLogoPath(self, key):
        return self.logoPaths[key]

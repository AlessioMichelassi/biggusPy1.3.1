import json
import os
import shutil
import sys
from os.path import exists

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.Menu.biggusMenu import BiggusMenu
from BiggusMain.biggusWidgets.canvas import Canvas
from BiggusMain.biggusWidgets.nodeBrowserWidget import NodeBrowser
from BiggusMain.biggusWidgets.terminalWidget import Terminal


class BiggusPy(QMainWindow):
    # ----------------- Variabili -----------------

    canvas: Canvas
    nodeBrowser: NodeBrowser
    terminal: Terminal

    statusMousePosition: QLabel
    path = "saveDir"
    fileName = "untitled"
    recentFilesMenu: BiggusMenu
    recentFiles = []

    # ----------------- sys Variables -----------------
    mainDir = "biggusFolder"
    configurationFilePath = "config.json"
    saveFileDirectory = "SaveDir"
    defaultNode = "defaultNode"
    nodesFolderPath = {}
    iconPaths = {}
    logoPaths = {}

    # ----------------- sys Variables -----------------

    configFontAndColors = {
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1620, 1300)
        self.setWindowTitle("BiggusPy(a great Caesar's friend) V0.1.3.1")
        self.setWindowIcon(QIcon('BiggusMain/elements/imgs/BiggusIcon.ico'))

    def start(self):
        self.initMainUI()
        self.initMenu()

    def initMainUI(self):
        # crea i widget
        self.canvas = Canvas(self)
        self.nodeBrowser = NodeBrowser(self, self.canvas)
        self.terminal = Terminal(self, self.canvas)
        mainSplit = QSplitter(Qt.Orientation.Vertical)
        mainSplit.addWidget(self.canvas)
        bottomSplit = QSplitter(Qt.Orientation.Horizontal)

        bottomSplit.addWidget(self.nodeBrowser)
        bottomSplit.addWidget(self.terminal)
        bottomSplit.setSizes([200, 200])
        mainSplit.addWidget(bottomSplit)
        mainSplit.setSizes([300, 100])
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

    # ------------------ config files ------------------

    def saveConfigFile(self):
        """
        ITA:
            Salva il file di configurazione.
        ENG:
            Save the configuration file.
        """
        fontAndColor = self.serializeFontAndColors()
        data = {
            "mainDir": self.mainDir,
            "configurationFilePath": self.configurationFilePath,
            "saveFileDirectory": self.saveFileDirectory,
            "iconPaths": self.iconPaths,
            "logoPaths": self.logoPaths,
            "nodesFolderPath": self.nodesFolderPath,
            "fontAndColor": fontAndColor
        }
        # salva il file di configurazione come pretty print
        data = json.dumps(data, indent=4)
        with open("config.json", "w") as f:
            f.write(data)

    def serializeFontAndColors(self):
        newDict = {}
        for key, value in self.configFontAndColors.items():
            if isinstance(value, QColor):
                # salva il valore rgba
                newDict[key] = f"({value.red()}, {value.green()}, {value.blue()}, {value.alpha()})"
            elif isinstance(value, QFont):
                # salva il valore della font
                newDict[key] = value.toString()
        return newDict

    @staticmethod
    def deserializeFontAndColors(dictionary):
        newDict = {}
        for key, value in dictionary.items():
            if isinstance(value, str):
                if value.startswith("("):
                    # carica il valore rgba
                    newDict[key] = QColor(value)
                elif value.startswith("QFont"):
                    newDict[key].fromString(value)
        return newDict

    def getMainDirectory(self):
        return self.mainDir

    # ------------------ return path ------------------

    def returnNodePath(self, key):
        try:
            path = self.nodesFolderPath[key]
            nodes_folder = os.path.abspath(path)
            relative_path = os.path.relpath(nodes_folder, os.getcwd())
            modulePath = f"{relative_path.replace('/', '.')}"
            return f"{relative_path}/"
        except KeyError:
            print(f"WARNING: {key} not found in nodesFolderPath, check the config file")
            print("content of nodesFolderPath:")
            print(f"{self.nodesFolderPath}")

    def returnIconPath(self, key):
        return self.iconPaths[key]

    def returnLogoPath(self, key):
        return self.logoPaths[key]

import json
import os
import sys

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
    mainDir = "Release/biggusFolder"
    configurationFilePath = "Release/config.json"
    saveFileDirectory = "Release/SaveDir"

    nodesFolderPath = {"python": "Release/biggusFolder/Nodes/PythonNodes",
                       "openCv": "Release/biggusFolder/Nodes/OpenCvNodes",
                       "pyQt5": "Release/biggusFolder/Nodes/PyQt5Nodes"}
    iconPaths = {
        "biggusIcon": "Release/biggusFolder/imgs/icon/biggusIcon",
        "pythonIcon": "Release/biggusFolder/imgs/icon/pythonIcon",
        "openCv": "Release/biggusFolder/imgs/icon/openCvIcon",
        "pyQt5": "Release/biggusFolder/imgs/icon/pyQt5Icon"}
    logoPaths = {
        "logos": "Release/biggusFolder/imgs/logos"}

    # ----------------- sys Variables -----------------

    configColor = {
        "systemFont": QFont("Lohit Gujarati", 16),
        "systemFontColor": QColor(250, 250, 250),

        "widgetFont": QFont("Lohit Gujarati", 14),
        "widgetFontColor": QColor(250, 250, 250),

        "widgetOnWidgetFont": QFont("Lohit Gujarati", 8),
        "widgetOnWidgetFontColor": QColor(150, 150, 240),

        "systemHighlightColor": QColor(60, 60, 65),
        "systemHighlightTextColor": QColor(250, 250, 255),
        "systemBorderColor": QColor(40, 40, 45),
        "systemBackgroundColor": QColor(50, 50, 53),
        "systemIconSize": 40,

        "widgetBorderColor": QColor(40, 40, 45),
        "widgetBackgroundColor": QColor(40, 40, 45),

        "widgetOnWidgetBorderColor": QColor(40, 40, 45),
        "widgetOnWidgetBackgroundColor": QColor(35, 35, 35)
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1920, 1100)
        self.setWindowTitle("BiggusPy(a great Caesar's friend) V0.1.3.1")
        self.setWindowIcon(QIcon('elements/imgs/BiggusIcon.ico'))
        # self.openConfigFile()
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
        mainSplit.setSizes([300,100])
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

    def setMainDirectory(self, _directory):
        self.mainDir = _directory
        self.nodesFolderPath = {}
        for folder in os.listdir(f"{self.mainDir}/Nodes"):
            if not os.path.isfile(f"{self.mainDir}/Nodes/{folder}"):
                # example: "python"
                key = folder
                # example: "Release/biggusFolder/Nodes/PythonNodes"
                value = f"{self.mainDir}/Nodes/{folder}"
                self.nodesFolderPath[key] = value
        self.iconPaths = {}
        for folder in os.listdir(f"{self.mainDir}/imgs/icon"):
            if not os.path.isfile(f"{self.mainDir}/imgs/icon/{folder}"):
                key = folder
                value = f"{self.mainDir}/imgs/icon/{folder}"
                self.iconPaths[key] = value
        self.logoPaths = {}
        for folder in os.listdir(f"{self.mainDir}/imgs/logo"):
            if not os.path.isfile(f"{self.mainDir}/imgs/logo/{folder}"):
                key = folder
                value = f"{self.mainDir}/imgs/logo/{folder}"
                self.logoPaths[key] = value

    def setBiggusConfigFile(self, _directory):
        self.configurationFilePath = f"{_directory}/config.json"

    def setBiggusSaveFileDirectory(self, _directory):
        self.saveFileDirectory = _directory

    def openConfigFile(self):
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
            self.iconPaths = data["iconPaths"]
            self.logoPaths = data["logoPaths"]
            self.nodesFolderPath = data["nodesFolderPath"]
        except FileNotFoundError:
            self.saveConfigFile()

    def saveConfigFile(self):
        """
        :return:
        """
        data = {"mainDir": self.mainDir,
                "iconPaths": self.iconPaths,
                "logoPaths": self.logoPaths,
                "nodesFolderPath": self.nodesFolderPath,
                "configurationFilePath": self.configurationFilePath,
                "saveFileDirectory": self.saveFileDirectory,
                "systemFont": self.systemFont,
                "systemFontColor": self.systemFontColor,
                "systemBackGroundColor": self.systemBackGroundColor,
                "systemBorderColor": self.systemBorderColor,
                "systemWidgetColor": self.systemWidgetColor,
                "wdgetFont": self.wdgetFont,
                "widgetFontSize": self.widgetFontSize,
                "systemWidgetBackGroundColor": self.systemWidgetBackGroundColor,
                "systemWidgetBorderColor": self.systemWidgetBorderColor,
                "systemHighlightColor": self.systemHighlightColor,
                "systemHighlightTextColor": self.systemHighlightTextColor,
                "widgetOnWidgetFontColor": self.widgetOnWidgetFontColor,
                "widgetOnWidgetFont": self.widgetOnWidgetFont,
                "widgetOnWidgetFontSize": self.widgetOnWidgetFontSize,
                "systemWidgetOnWidgetBackGroundColor": self.systemWidgetOnWidgetBackGroundColor}

        with open("config.json", "w") as f:
            json.dump(data, f)

    def getMainDirectory(self):
        return self.mainDir

    # ------------------ return path ------------------

    def returnNodePath(self, key):
        path = self.nodesFolderPath[key]
        nodes_folder = os.path.abspath(path)
        relative_path = os.path.relpath(nodes_folder, os.getcwd())
        modulePath = f"{relative_path.replace('/', '.')}"
        return f"{relative_path}/"

    def returnIconPath(self, key):
        return self.iconPaths[key]

    def returnLogoPath(self, key):
        return self.logoPaths[key]

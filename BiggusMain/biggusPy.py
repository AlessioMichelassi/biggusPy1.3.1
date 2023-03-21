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

    nodesFolderPath = {"python": "biggusFolder/Nodes/PythonNodes",
                       "openCv": "biggusFolder/Nodes/OpenCvNodes",
                       "pyQt5": "biggusFolder/Nodes/PyQt5Nodes"}
    iconPaths = {
        "biggusIcon": "Release/biggusFolder/imgs/icon/biggusIcon",
        "pythonIcon": "Release/biggusFolder/imgs/icon/pythonIcon",
        "openCv": "Release/biggusFolder/imgs/icon/openCvIcon",
        "pyQt5": "Release/biggusFolder/imgs/icon/pyQt5Icon"}
    logoPaths = {
        "logos": "Release/biggusFolder/imgs/logos"}

    # ----------------- sys Variables -----------------

    configFontAndColors = {
        "systemFont": QFont("MS Shell Dlg 2", 16),
        "systemFontColor": QColor(250, 250, 250),

        "widgetFont": QFont("MS Shell Dlg 2", 14),
        "widgetFontColor": QColor(250, 250, 250),

        "widgetOnWidgetFont": QFont("MS Shell Dlg 2", 8),
        "widgetOnWidgetFontColor": QColor(150, 150, 240),

        "systemHighlightColor": QColor(60, 60, 65),
        "systemHighlightTextColor": QColor(250, 250, 255),
        "systemBorderColor": QColor(40, 40, 45),
        "systemBackgroundColor": QColor(50, 50, 53),
        "systemIconSize": 40,

        "widgetBorderColor": QColor(40, 40, 45),
        "widgetBackgroundColor": QColor(39, 39, 40),

        "widgetOnWidgetBorderColor": QColor(40, 40, 45),
        "widgetOnWidgetBackgroundColor": QColor(43, 43, 45)
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1620, 1300)
        self.setWindowTitle("BiggusPy(a great Caesar's friend) V0.1.3.1")
        # se è windows
        if os.name == "nt":
            self.setWindowIcon(QIcon('BiggusMain/elements/imgs/BiggusIcon.ico'))
        else:
            self.setWindowIcon(QIcon('BiggusMain/elements/imgs/BiggusIcon.ico'))
        self.openConfigFile()
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

    def setMainDirectoryMacLinux(self, _directory):
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

    def setMainDirectoryWinNT(self, _directory):
        self.mainDir = _directory
        self.nodesFolderPath = {}
        for folder in os.listdir(f"{self.mainDir}\\Nodes"):
            if not os.path.isfile(f"{self.mainDir}\\Nodes\\{folder}"):
                # example: "python"
                key = folder
                # example: "Release/biggusFolder/Nodes/PythonNodes"
                value = f"{self.mainDir}\\Nodes\\{folder}"
                self.nodesFolderPath[key] = value
        self.iconPaths = {}
        for folder in os.listdir(f"{self.mainDir}\\imgs\\icon"):
            if not os.path.isfile(f"{self.mainDir}\\imgs\\icon\\{folder}"):
                key = folder
                value = f"{self.mainDir}\\imgs\\icon\\{folder}"
                self.iconPaths[key] = value
        self.logoPaths = {}
        for folder in os.listdir(f"{self.mainDir}\\imgs\\logo"):
            if not os.path.isfile(f"{self.mainDir}\\imgs\\logo\\{folder}"):
                key = folder
                value = f"{self.mainDir}\\imgs\\logo\\{folder}"
                self.logoPaths[key] = value

    def setBiggusConfigFile(self, _directory):
        self.configurationFilePath = f"{_directory}/config.json"

    def setBiggusSaveFileDirectory(self, _directory):
        self.saveFileDirectory = _directory

    def openConfigFile(self):
        print("Opening configuration file...")
        if exists("config.json"):
            print(f"Configuration file found at {os.getcwd()}\\config.json")
            with open("config.json", "r") as f:
                data = json.load(f)
        else:
            print("Configuration file not found, a new configuration file will be created.")
            openFileDialog = QFileDialog()
            openFileDialog.setFileMode(QFileDialog.Directory)
            openFileDialog.setOption(QFileDialog.ShowDirsOnly)
            if openFileDialog.exec_():
                filename = openFileDialog.selectedFiles()[0]
                with open(filename, "r") as f:
                    data = json.load(f)


    def openConfigFileOld(self):
        print("Apertura file di configurazione...")
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
        except Exception as e:
            print("File di configurazione non trovato, verrà creato un nuovo file di configurazione.")
            openDialog = QFileDialog()
            openDialog.setFileMode(QFileDialog.Directory)
            openDialog.setOption(QFileDialog.ShowDirsOnly)
            if openDialog.exec_():
                configFile = openDialog.selectedFiles()[0]
                with open(configFile,"r"):
                    data = json.load(f)
            self.mainDir = data["mainDir"]
            if os.name == "nt":
                self.mainDir = data["mainDir"]
                if getattr(sys, "frozen", False):
                    # Il programma è stato compilato in un eseguibile autonomo.
                    # Il percorso dell'eseguibile è in sys.executable.
                    print("software compilato in un eseguibile autonomo")
                    self.mainDir = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "biggusFolder"))
                    print(f"Original main dir: {data['mainDir']}")
                    print(f"New main dir: {self.mainDir}")

                    biggusFolderSrc = os.path.join(self.mainDir)
                    print(f"biggusFolderSrc: {biggusFolderSrc} copy to:")
                    biggusTempDest = os.path.join(sys._MEIPASS, "biggusFolder")
                    print(f"biggusTempDest: {biggusTempDest}")
                    if shutil.copytree(biggusFolderSrc, biggusTempDest):
                        print("biggusFolder copied")
                    else:
                        print("biggusFolder not copied")
                else:
                    # Il programma è stato eseguito da un file sorgente.
                    print("software eseguito da un file sorgente")
                    self.mainDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "biggusFolder"))
                module_path = self.mainDir
                os.environ["PYTHONPATH"] = os.pathsep.join([os.environ.get("PYTHONPATH", ""), module_path])
                sys.path.insert(0, module_path)

            self.configurationFilePath = data["configurationFilePath"]
            self.saveFileDirectory = data["saveFileDirectory"]
            self.iconPaths = data["iconPaths"]
            self.logoPaths = data["logoPaths"]
            self.nodesFolderPath = data["nodesFolderPath"]
            configFontAndColors = data["fontAndColor"]
            for key, value in configFontAndColors.items():
                # se è un font è tipo "font": "MS Shell Dlg 2,8,-1,5,50,0,0,0,0,0",
                # se è un colore è tipo: "systemFontColor": "(250, 250, 250, 255)",
                if "Color" in key:
                    # se è un colore
                    value = value.replace("(", "")
                    value = value.replace(")", "")
                    value = value.split(",")
                    value = [int(i) for i in value]
                    value = QColor(*value)
                else:
                    # se è un font
                    QFont(value)

            self.saveConfigFile()

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
                newDict["font"] = value.toString()
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
        path = self.nodesFolderPath[key]
        nodes_folder = os.path.abspath(path)
        relative_path = os.path.relpath(nodes_folder, os.getcwd())
        modulePath = f"{relative_path.replace('/', '.')}"
        return f"{relative_path}/"

    def returnIconPath(self, key):
        return self.iconPaths[key]

    def returnLogoPath(self, key):
        return self.logoPaths[key]

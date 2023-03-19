import configparser
import json
import pprint
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from BiggusMain.Menu.openCvNodeMenu import OpenCvNodeMenu
from BiggusMain.Menu.preferenceWidget import PreferenceWidget
from BiggusMain.Menu.pyQt5NodeMenu import PyQt5NodeMenu
from BiggusMain.Menu.pythonNodeMenu import PythonNodeMenu
from BiggusMain.biggusWidgets.CodeToNodeWidget.codeToNode import FromCodeToNode
from scratchONodeV0_9.scratchNode import scratchNodeV0_9


class BiggusMenu(QMenuBar):
    # Menu Variables
    fileMenu: QMenu
    editMenu: QMenu
    nodeMenu: QMenu
    viewMenu: QMenu
    helpMenu: QMenu
    recentFilesMenu: QMenu

    pythonNodeMenu: QMenu
    openCvNodeMenu: QMenu
    pyQt5NodeMenu: QMenu

    # software link variables
    biggusPy: 'mainGraphicEditorWindows'
    canvas: 'canvas'
    graphicView: 'graphicView'
    graphicScene: 'graphicScene'
    ScratchONode: 'ScratchONode'

    # systemVariables
    recentFiles: list
    systemPath: str
    recentFiles = []

    fileName = "untitled"
    availableNodes = []

    def __init__(self, biggusPy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.biggusPy = biggusPy
        self.createMenu()
        self.createFileMenu()
        self.createEditMenu()
        self.createNodeMenu()
        self.createViewMenu()
        self.createHelpMenu()
        self.setMenuStyle()

    def createLink(self):
        self.canvas = self.biggusPy.canvas
        self.graphicView = self.biggusPy.graphicView
        self.graphicScene = self.biggusPy.graphicScene
        self.ScratchONode = self.biggusPy.ScratchONode

    def createMenu(self):
        self.fileMenu = self.addMenu("&File")
        self.editMenu = self.addMenu("&Edit")
        self.nodeMenu = self.addMenu("&Node")
        self.viewMenu = self.addMenu("&View")
        self.helpMenu = self.addMenu("&Help")

    def createFileMenu(self):
        """
        create the file menu with New, open, openRecent, save, saveAs, exit
        :return:
        """
        _new = QAction("New", self)
        _new.setShortcut("Ctrl+N")
        _new.setStatusTip("Create a new file")
        _new.triggered.connect(self.newFile)
        _open = QAction("Open", self)
        _open.setShortcut("Ctrl+O")
        _open.setStatusTip("Open a file")
        _open.triggered.connect(self.openFile)

        self.recentFilesMenu = QMenu('Recent Files', self)
        self.recentFiles = self.loadRecentFiles()
        self.recentFilesMenu.triggered.connect(self.openRecentFile)
        _save = QAction("Save", self)
        _save.setShortcut("Ctrl+S")
        _save.setStatusTip("Save the file")
        _save.triggered.connect(self.saveFile)
        _saveAs = QAction("Save As", self)
        _saveAs.setShortcut("Ctrl+Shift+S")
        _saveAs.setStatusTip("Save the file as")
        _saveAs.triggered.connect(self.saveAsFile)
        _exit = QAction("Exit", self)
        _exit.setShortcut("Ctrl+Q")
        _exit.setStatusTip("Exit the application")

        _exit.triggered.connect(self.exitApp)

        self.fileMenu.addAction(_new)
        self.fileMenu.addAction(_open)
        self.fileMenu.addMenu(self.recentFilesMenu)
        self.updateRecentFileMenu()
        self.fileMenu.addAction(_save)
        self.fileMenu.addAction(_saveAs)
        self.fileMenu.addAction(_exit)

    def createEditMenu(self):
        """
        create the edit menu with undo, redo, copy, paste, delete
        :return:
        """
        _undo = QAction("Undo", self)
        _undo.setShortcut("Ctrl+Z")
        _undo.setStatusTip("Undo the last action")
        _redo = QAction("Redo", self)
        _redo.setShortcut("Ctrl+Shift+Z")
        _redo.setStatusTip("Redo the last action")
        _copy = QAction("Copy", self)
        _copy.setShortcut("Ctrl+C")
        _copy.setStatusTip("Copy the selected item")
        _copy.triggered.connect(self.copy)
        _paste = QAction("Paste", self)
        _paste.setShortcut("Ctrl+V")
        _paste.setStatusTip("Paste the copied item")
        _paste.triggered.connect(self.paste)
        _delete = QAction("Delete", self)
        _delete.setShortcut("Del")
        _delete.setStatusTip("Delete the selected item")
        _delete.triggered.connect(self.delete)
        _selectAll = QAction("Select All", self)
        _selectAll.setShortcut("Ctrl+A")
        _selectAll.setStatusTip("Select all the items")
        _selectAll.triggered.connect(self.selectAll)
        self.editMenu.addAction(_undo)
        self.editMenu.addAction(_redo)
        self.editMenu.addAction(_copy)
        self.editMenu.addAction(_paste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(_delete)
        self.editMenu.addSeparator()
        self.editMenu.addAction(_selectAll)

    def createNodeMenu(self):
        """
        create the biggusNode menu with addNode, removeNode, renameNode
        :return:
        """
        self.pythonNodeMenu = PythonNodeMenu(self, self.biggusPy)

        self.pyQt5NodeMenu = PyQt5NodeMenu(self, self.biggusPy)

        self.openCvNodeMenu = OpenCvNodeMenu(self, self.biggusPy)

        self.nodeMenu.addMenu(self.pythonNodeMenu)
        self.nodeMenu.addMenu(self.pyQt5NodeMenu)
        self.nodeMenu.addMenu(self.openCvNodeMenu)
        self.nodeMenu.addSeparator()
        action1 = self.nodeMenu.addAction("refresh biggusNode list")
        action1.triggered.connect(self.refreshNodeList)
        self.nodeMenu.addAction(action1)
        self.nodeMenu.addSeparator()
        action2 = self.nodeMenu.addAction("from code to biggusNode")
        action2.triggered.connect(self.fromCodeToNode)
        self.availableNodes = self.pythonNodeMenu.availableNodeList + \
                              self.pyQt5NodeMenu.availableNodeList + \
                              self.openCvNodeMenu.availableNodeList

    def createViewMenu(self):
        """
        create the view menu with zoomIn, zoomOut, zoomReset
        :return:
        """
        _zoomIn = QAction("Zoom In", self)
        _zoomIn.setShortcut("Ctrl+Shift+Up")
        _zoomIn.setStatusTip("Zoom in")
        _zoomIn.triggered.connect(self.zoomIn)
        _zoomOut = QAction("Zoom Out", self)
        _zoomOut.setShortcut("Ctrl+Shift+Down")
        _zoomOut.setStatusTip("Zoom out")
        _zoomOut.triggered.connect(self.zoomOut)
        _zoomReset = QAction("Zoom Reset", self)
        _zoomReset.setShortcut("Ctrl+Shift+Left")
        _zoomReset.setStatusTip("Zoom reset")
        _zoomReset.triggered.connect(self.zoomReset)

        _zoomFitInView = QAction("Zoom Fit In View", self)
        _zoomFitInView.setShortcut("f")
        _zoomFitInView.setStatusTip("Zoom Fit In View")
        _zoomFitInView.triggered.connect(self.zoomFitInView)
        _settings = QAction("Settings", self)
        _settings.setShortcut("Ctrl+Shift+Right")
        _settings.setStatusTip("Settings")
        _settings.triggered.connect(self.settings)

        _scratchONode = QAction("Scratch O Node", self)
        _scratchONode.setStatusTip("open the Scratch O Node Editor")
        _scratchONode.triggered.connect(self.openScratchONode)
        self.viewMenu.addAction(_zoomIn)
        self.viewMenu.addAction(_zoomOut)
        self.viewMenu.addAction(_zoomReset)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(_zoomFitInView)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(_settings)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(_scratchONode)

    def createHelpMenu(self):
        _help = QAction("Help", self)
        _help.setStatusTip("Help")
        _help.triggered.connect(self.help)
        _about = QAction("About", self)
        _about.setStatusTip("About")
        _about.triggered.connect(self.about)
        _aboutQt = QAction("About Qt", self)
        _aboutQt.setStatusTip("About Qt")
        _aboutQt.triggered.connect(self.aboutQt)
        self.helpMenu.addAction(_help)
        self.helpMenu.addAction(_about)
        self.helpMenu.addAction(_aboutQt)

    def doAboutMenu(self, arg0, arg1, arg2):
        result = QAction(arg0, self)
        result.setShortcut(arg1)
        result.setStatusTip(arg2)
        return result

    # ------------------- File Menu -------------------

    def newFile(self):
        self.biggusPy.restartCanvas()
        # self.biggusPy.printOnStatusBar("new")
        self.fileName = "Untitled"

    def openFile(self):  # sourcery skip: extract-method
        self.newFile()
        openDialog = QFileDialog(self, "Open a file")
        if openDialog.exec() != QDialog.DialogCode.Accepted:
            return
        openDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file = openDialog.selectedFiles()[0]
        try:
            with open(file, "r") as f:
                file = f.read()
            self.biggusPy.canvas.deserialize(file)
            fileName = openDialog.selectedFiles()[0].split("/")[-1].split(".")[0]
            print(fileName)
            # self.biggusPy.printOnStatusBar(f"File opened {self.fileName}")
            self.saveRecentFiles([openDialog.selectedFiles()[0]])
            self.updateRecentFileMenu()
        except Exception as e:
            print(e)
            # self.biggusPy.printOnStatusBar("Error opening file")

    def openRecentFile(self, action):
        # sourcery skip: use-named-expression
        filename = action.text()  # ottiene il nome del file dall'action
        with open(filename, "r") as f:
            file = f.read()
        self.biggusPy.canvas.deserialize(file)
        self.fileName = filename
        # self.biggusPy.printOnStatusBar(f"File opened {self.fileName}")
        self.saveRecentFiles([filename])
        self.updateRecentFileMenu()

    def saveFile(self):
        fileData = self.biggusPy.canvas.serialize()
        if self.fileName == "untitled":
            self.saveAsFile()
        else:
            with open(self.fileName, "w") as f:
                f.write(fileData)
            # self.biggusPy.printOnStatusBar(f"File saved as {self.fileName}")

    def saveAsFile(self):
        dialog = QFileDialog.getSaveFileName(self, "Save as", self.biggusPy.path, "Json (*.json)")
        if not dialog[0]:
            return
        filename = dialog[0]
        file = QFile(filename)
        if not file.open(QFile.OpenModeFlag.WriteOnly | QFile.OpenModeFlag.Text):
            reason = file.errorString()
            QMessageBox.warning(self, "Dock Widgets",
                                f"Cannot write file {filename}:\n{reason}.")
            return
        with open(filename, "w") as f:
            f.write(self.biggusPy.canvas.serialize())
        # self.biggusPy.printOnStatusBar(f"File saved as {self.fileName}")
        self.saveRecentFiles([filename])
        self.updateRecentFileMenu()

    def exitApp(self):
        sys.exit()

    # ------------------- Edit Menu -------------------

    def undo(self):
        print("undo")

    def redo(self):
        print("redo")

    def copy(self):
        self.biggusPy.canvas.graphicView.copyNode()

    def paste(self):
        self.biggusPy.canvas.pasteNode()

    def delete(self):
        self.biggusPy.canvas.graphicView.deleteSelectedItems()

    def selectAll(self):
        self.biggusPy.canvas.graphicView.selectAllItems()

    # ------------------- Node Menu -------------------

    def refreshNodeList(self):
        self.pythonNodeMenu.updateNodeMenu()
        self.pyQt5NodeMenu.updateNodeMenu()
        self.openCvNodeMenu.updateNodeMenu()

    def fromCodeToNode(self):
        fromCodeToNodeWindow = FromCodeToNode(self.biggusPy.canvas, self.biggusPy)
        fromCodeToNodeWindow.show()

    def addNode(self):
        print("add biggusNode")

    def removeNode(self):
        print("remove biggusNode")

    def renameNode(self):
        print("rename biggusNode")

    # ------------------- View Menu -------------------

    def zoomIn(self):
        self.biggusPy.canvas.graphicView.scale(1.3, 1.3)

    def zoomOut(self):
        self.biggusPy.canvas.graphicView.scale(0.8, 0.8)

    def zoomReset(self):
        self.biggusPy.canvas.graphicView.scaleScene(1)

    def zoomFitInView(self):
        self.biggusPy.canvas.graphicView.selectAllCenterSceneAndDeselect()

    def settings(self):
        self.preferencesWidget = PreferenceWidget(self.biggusPy)
        self.preferencesWidget.show()

    def openScratchONode(self):
        scratchNode = scratchNodeV0_9(self.biggusPy.canvas)
        scratchNode.filePath = "Release/biggusFolder/biggusCode/defaultNode.py"
        scratchNode.loadUntitledNode(scratchNode.filePath)
        scratchNode.show()

    # ------------------- Help Menu -------------------

    def help(self):
        pass

    def about(self):
        aboutDialog = QDialog(self)
        aboutDialog.setWindowTitle("About BiggusPy")
        aboutDialog.setFixedSize(800, 500)

        titleLabel = QLabel("BiggusPy - a great Caesar friend")
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        versionLabel = QLabel("Version 0.2 - alpha")
        versionLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        authorLabel = QLabel("Author: Alessio Michelassi (2023)")
        authorLabel.setStyleSheet("font-size: 12px; font-weight: bold;")
        descriptionTxt = QTextEdit()
        descriptionTxt.setStyleSheet("font-size: 14px;")
        with open("BiggusMain/Menu/AboutThisSoftware", "r") as file:
            aboutTxt = file.read()
        descriptionTxt.setText(aboutTxt)
        # mette il testo giustificato al centro
        descriptionTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        descriptionTxt.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(titleLabel)
        layout.addWidget(versionLabel)
        layout.addWidget(descriptionTxt)
        aboutDialog.setLayout(layout)

        # Visualizzazione della finestra di dialogo
        aboutDialog.exec_()

    def aboutQt(self):
        """
            ITA: Mostra la finestra di About Qt
            ENG: Show the About Qt window
        :return:
        """
        QMessageBox.aboutQt(self, "About Qt")

    # ------------------ recent files ------------------

    @staticmethod
    def saveRecentFiles(recentFiles):
        config = configparser.ConfigParser()
        config['recentFiles'] = {'files': ','.join(recentFiles)}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def loadRecentFiles():
        """
        get the recent files
        :return:
        """
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            recentFiles = config['recentFiles']['files'].split(',')
            return [] if recentFiles == [''] else recentFiles
        except:
            return []

    def clearRecentFiles(self):
        """
        clear the recent files
        :return:
        """
        self.saveRecentFiles([])
        self.updateRecentFileMenu()

    def updateRecentFileMenu(self):
        """
        update the recent file menu
        :return:
        """
        self.recentFilesMenu.clear()
        recentFiles = self.loadRecentFiles()
        if len(recentFiles) == 0:
            self.recentFilesMenu.addAction("No recent files")
        else:
            for file in recentFiles:
                self.recentFilesMenu.addAction(file)
        self.recentFilesMenu.addSeparator()
        self.recentFilesMenu.addAction("Clear recent files").triggered.connect(self.clearRecentFiles)

    # ------------------ style ------------------

    def setMenuStyle(self):
        """
        set the menu style
        :return:
        """
        # #2D2D30 è  in rgb 45 45 48
        self.setStyleSheet(f"""
        QMenu {{
                font-family: "{self.biggusPy.configColor["systemFont"].family()}";
                font-size: {self.biggusPy.configColor["systemFont"].pointSize()}px;
                background-color: #2D2D30;
                border: 1px solid #2D2D30;
                color: #FFFFFF;
            }}
            QMenu::item {{
                background-color: transparent;
                padding: 5px 30px 5px 30px;
            }}
            QMenu::item:selected {{
                background-color: #3A393C;
                color: #FFFFFF;
            }}
            QMenu::separator {{
                height: 1px;
                background-color: #3A393C;
                margin-left: 10px;
                margin-right: 5px;
            }}""")

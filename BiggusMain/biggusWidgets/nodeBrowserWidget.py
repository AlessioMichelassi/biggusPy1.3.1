import os
from os.path import exists

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.biggusWidgets.customFocusWidget import customFocusWidget
from BiggusMain.biggusWidgets.draggableWidget import DraggableWidget


class NodeBrowser(customFocusWidget):
    pyTab: QWidget
    qtTab: QWidget
    cvTab: QWidget
    tabWidget: QTabWidget

    def __init__(self, biggusPy, canvas, parent=None):
        super().__init__(biggusPy, parent)
        self.canvas = canvas
        self.initUI()

    def initUI(self):
        pythonNodeFolderPath = self.biggusPy.returnNodePath("python")
        pyQt5NodeFolderPath = self.biggusPy.returnNodePath("pyQt5")
        openCvNodeFolderPath = self.biggusPy.returnNodePath("openCv")

        self.tabWidget = QTabWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        self.setLayout(mainLayout)
        if exists(pythonNodeFolderPath):
            self.addTabPage("python", pythonNodeFolderPath)
        if exists(pyQt5NodeFolderPath):
            self.addTabPage("pyqt5", pyQt5NodeFolderPath)
        if exists(openCvNodeFolderPath):
            self.addTabPage("opencv", openCvNodeFolderPath)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def addTabPage(self, name, itemList):
        scroll_area = QScrollArea(self.tabWidget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        widget = QWidget(scroll_area)
        scroll_area.setWidget(widget)

        grid = QGridLayout(widget)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        grid.setContentsMargins(10, 10, 10, 10)
        Nodes = []
        for _file in os.listdir(itemList):
            if _file.endswith('.py'):
                Nodes.append(_file[:-3])
                draggableObj = DraggableWidget(_file[:-3], widget)
                draggableObj.nodePath = itemList
                try:
                    path = self.biggusPy.returnIconPath(_file[:-3])
                    file = path + (_file[:-3].replace("Node", "")).lower() + ".ico"
                    if os.path.isfile(file):
                        draggableObj.setIcon(file)
                except Exception as e:
                    a = e
                    path = f'{self.biggusPy.returnIconPath("biggusIcon")}/BiggusIcon.ico'
                    draggableObj.setIcon(path)
                row, col = divmod(len(Nodes), 8)
                grid.addWidget(draggableObj, row, col, Qt.AlignHCenter | Qt.AlignVCenter)
                col += 1
                if col > 7:
                    col = 0
                    row += 1
            # Imposta una dimensione fissa per i widget nel layout
            for i in range(grid.count()):
                item = grid.itemAt(i)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setFixedSize(100, 100)

            self.tabWidget.addTab(scroll_area, name)

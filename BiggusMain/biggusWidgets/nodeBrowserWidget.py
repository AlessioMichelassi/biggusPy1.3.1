import os
from os.path import exists

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.biggusWidgets.customFocusWidget import customFocusWidget


class DraggableWidget(QWidget):
    dragStartPos = None
    lblTxt: QLabel
    lblIcon: QLabel
    mainLayout: QVBoxLayout
    node = None
    nodePath: str = None

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.lblTxt = QLabel(self.title)
        self.lblIcon = QLabel()
        self.lblIcon.setPixmap(QPixmap("elements/imgs/BiggusIcon.ico"))
        self.lblIcon.setScaledContents(True)
        self.lblIcon.setFixedSize(64, 40)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.lblIcon, Qt.AlignmentFlag.AlignHCenter)
        self.mainLayout.addWidget(self.lblTxt, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.mainLayout)
        self.setStyleSheet("font-family: Lohit Gujarati; "
                           "font-size: 8pt; "
                           "background-color: transparent; "
                           "color: black;")

    def setIcon(self, path):
        self.lblIcon.setPixmap(QPixmap(path))
        self.lblIcon.setScaledContents(True)
        self.lblIcon.setFixedSize(64, 40)
        self.lblIcon.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.lblIcon.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # Salva la posizione di partenza del drag
            self.dragStartPos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            print(f"Debug from class {self.__class__.__name__}: mouseMoveEvent")
            # Crea l'oggetto drag
            drag = QDrag(self)
            mime_data = QMimeData()
            mimeString = f"{self.nodePath};;{self.title}"
            mime_data.setText(mimeString)
            drag.setMimeData(mime_data)

            # Crea l'icona del drag
            iconSize = self.lblIcon.size()
            pixmap = QPixmap(iconSize)
            pixmap.fill(Qt.GlobalColor.transparent)
            self.lblIcon.render(pixmap)

            drag.setPixmap(pixmap)
            drag.setHotSpot(self.dragStartPos - self.rect().topLeft())

            # Esegui il drag
            drag.exec_(Qt.DropAction.MoveAction | Qt.DropAction.CopyAction, Qt.DropAction.CopyAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()


class NodeBrowser(customFocusWidget):
    systemFont: QFont = QFont("Lohit Gujarati", 8)
    pyTab: QWidget
    qtTab: QWidget
    cvTab: QWidget

    def __init__(self, biggus, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.biggusPy = biggus
        pythonNodeFolderPath = self.biggusPy.returnPath("python")
        pyQt5NodeFolderPath = self.biggusPy.returnPath("pyQt5")
        openCvNodeFolderPath = self.biggusPy.returnPath("openCv")
        self.setFont(self.systemFont)
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
        Nodes = []
        for _file in os.listdir(itemList):
            if _file.endswith('.py'):
                Nodes.append(_file[:-3])
                draggableObj = DraggableWidget(_file[:-3], widget)
                draggableObj.nodePath = itemList
                path = r"Release/biggusFolder/imgs/icon/"
                file = path + (_file[:-3].replace("Node", "")).lower() + ".ico"
                if os.path.isfile(file):
                    draggableObj.setIcon(file)
                else:
                    draggableObj.setIcon("BiggusMain/elements/imgs/BiggusIcon.ico")
                row, col = divmod(len(Nodes), 8)
                grid.addWidget(draggableObj, row, col)
        self.tabWidget.addTab(scroll_area, name)

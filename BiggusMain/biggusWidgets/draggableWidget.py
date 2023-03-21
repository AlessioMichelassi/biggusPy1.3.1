from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

    def initUI(self):
        self.lblTxt = QLabel(self.title)
        self.lblIcon = QLabel()
        self.lblIcon.setPixmap(QPixmap("elements/imgs/BiggusIcon.ico"))
        self.lblIcon.setScaledContents(True)
        self.lblIcon.setFixedSize(50, 40)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.lblIcon, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.mainLayout.addWidget(self.lblTxt, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.mainLayout)
        self.setStyleSheet("font-family: Lohit Gujarati; "
                           "font-size: 8pt; "
                           "background-color: transparent; "
                           "color: lightgray; ")

    def setIcon(self, path):
        self.lblIcon.setPixmap(QPixmap(path))
        self.lblIcon.setScaledContents(True)
        self.lblIcon.setFixedSize(54, 40)
        self.lblIcon.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # Salva la posizione di partenza del drag
            self.dragStartPos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
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

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.elements.Connections.Connection import Connection
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeGraphicV1_2 import AbstractNodeGraphic


class GraphicSceneOverride(QGraphicsScene):
    colorBackground: QColor = QColor(39, 39, 39, 255)
    greyLighter: QColor = QColor(47, 47, 47, 255)
    greyDarker = QColor = QColor(29, 29, 29, 255)
    currentMousePos = QPointF(0, 0)

    def __init__(self, parent=None):
        super().__init__(parent)

        # set the grid Size
        self.smallGridSize = 10
        self.bigGridSize = 50

        # set the color of the scene
        self.setBackgroundBrush(self.colorBackground)
        self._penLight = QPen(self.greyLighter)
        self._penLight.setWidth(1)
        self._penDark = QPen(self.greyDarker)
        self._penDark.setWidth(2)
        self.currentDraggingNode = None
        self.currentHoveredItem = None

    def setGraphicSceneSize(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)

        _left = int(rect.left())
        _right = int(rect.right())
        _top = int(rect.top())
        _bottom = int(rect.bottom())

        lightGreyLines, darkGreyLines = [], []
        firstVerticalLine = _left - (_left % self.smallGridSize)
        firstHorizontalLine = _top - (_top % self.smallGridSize)

        for x in range(firstVerticalLine, _right, self.smallGridSize):
            if x % self.bigGridSize == 0:
                darkGreyLines.append(QLine(x, _top, x, _bottom))
            else:
                lightGreyLines.append(QLine(x, _top, x, _bottom))

        for y in range(firstHorizontalLine, _bottom, self.smallGridSize):
            if y % self.bigGridSize == 0:
                darkGreyLines.append(QLine(_left, y, _right, y))
            else:
                lightGreyLines.append(QLine(_left, y, _right, y))
        painter.setPen(self._penLight)
        if lightGreyLines:
            painter.drawLines(*lightGreyLines)
        painter.setPen(self._penDark)
        if darkGreyLines:
            painter.drawLines(*darkGreyLines)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            item = self.itemAt(event.scenePos(), QTransform())
            if isinstance(item, AbstractNodeGraphic):
                self.currentDraggingNode = item
                self.currentDraggingNode.setSelected(True)
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseMoveEvent(event)
        self.currentMousePos = event.scenePos()
        if self.currentDraggingNode is not None:
            mime_data = QMimeData()
            drag = QDrag(self.views()[0])
            drag.setMimeData(mime_data)
            drag.exec_(Qt.DropAction.MoveAction)
            event.accept()
            return
        item = self.itemAt(event.scenePos(), QTransform())
        self.currentHoveredItem = item if isinstance(item, Connection) else None

    def mouseReleaseEvent(self, event):
        if self.currentDraggingNode is not None:
            self.currentDraggingNode.setSelected(False)
            middleNode = self.currentDraggingNode.nodeInterface
            self.currentDraggingNode = None

            if self.currentHoveredItem is not None and isinstance(self.currentHoveredItem, Connection):
                startNode = self.currentHoveredItem.outputNode
                startPlug = self.currentHoveredItem.outputPlug
                startPlugIndex = self.currentHoveredItem.outIndex

                new_connection = Connection(startNode, startPlug, startPlugIndex, middleNode, middleNode.inPlugs[0], 0)
                self.addItem(new_connection)

                endNode = self.currentHoveredItem.inputNode
                endPlug = self.currentHoveredItem.inputPlug
                endPlugIndex = self.currentHoveredItem.inIndex
                new_connection = Connection(middleNode, middleNode.outPlugs[0], 0, endNode, endPlug, endPlugIndex)
                self.addItem(new_connection)
                event.accept()
                return

        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        # find item at these coordinates
        item = self.itemAt(e.scenePos())
        if item.setAcceptDrops == True:
            # pass on event to item at the coordinates
            try:
                item.dropEvent(e)
            except RuntimeError:
                pass  # This will supress a Runtime Error generated when dropping into a widget with no MyProxy

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

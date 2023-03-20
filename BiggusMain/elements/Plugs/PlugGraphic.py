from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class SuperTxtTitle(QGraphicsTextItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def setColor(self, color):
        self.setDefaultTextColor(color)

    def setText(self, txt):
        self.parent.plugData.setNameFromGraphic(txt)

    def eventFilter(self, obj, event):
        # Verifica se l'evento è una pressione del tasto Invio
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            # Esegue l'azione desiderata (ad esempio, imposta il nuovo valore del testo)
            self.setText(self.toPlainText().strip())
            return True
        return super().eventFilter(obj, event)


class PlugGraphic(QGraphicsItem):
    txtTitle: QGraphicsTextItem
    plugData = None
    isLocked = True
    isGraphicalRenamePermitted = False
    nodeGraphic = None
    isTxtReversed = False

    def __init__(self, plugData, diameter=8, parent=None):
        """
        ITA:
            Questa classe rappresenta la grafica di un plug. Ovvero un cerchio bianco con un altro cerchio nero
            all'interno. Ha un testo che rappresenta il nome del plug e può essere cambiato cliccando con il tasto
            in modalità editor, oppure in hardcode.
        ENG:
            This class represents the graphic of a plug. That is, a white circle with another black circle
            inside. It has a text that represents the name of the plug and can be changed by clicking with the button
            in editor mode, or in hardcode.
        :param plugData:
        :param diameter:
        :param parent:
        """
        super().__init__(parent)
        self.diameter = diameter
        self.plugData = plugData
        self.nodeGraphic = parent
        self.nodeInterface = self.nodeGraphic.nodeInterface
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.boundingRectangle = QRectF(-self.diameter // 2, -self.diameter // 2, self.diameter * 2, self.diameter * 2)
        self.setZValue(4)
        self.createTitleText()

    def __str__(self):
        """
        ITA:
            Questo metodo viene chiamato quando si fa un print di un oggetto di questa classe,
            tenendo premuto CTRL + Click sull'oggetto, vengono stampate le informazioni del plug.
        ENG:
            This method is called when you do a print of an object of this class,
            holding down CTRL + Click on the object, the plug information is printed.
        :return:
        """
        returnValue = f"{self.plugData.getTitle()}: {self.plugData.getValue()}\n"
        returnCode = f"{self.plugData.getCode()}\n"
        returnPlug = f"[{self.title}] = {self.plugData.getValue()} index = {self.plugData.index}\n"
        return returnValue + returnCode + returnPlug

    @property
    def name(self):
        return self.plugData.className

    @property
    def title(self):
        return f"{self.plugData.getTitle()}"

    def getNode(self):
        return self.nodeGraphic.nodeInterface

    def getClassName(self):
        return self.plugData.className

    def createTitleText(self):
        font = QFont()
        font.setPointSize(10)
        self.txtTitle = SuperTxtTitle(self)
        self.txtTitle.setFont(font)
        self.txtTitle.installEventFilter(self.txtTitle)
        # self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.txtTitle.setPlainText(self.title)
        # Posiziona la label 20 pixel sopra il centro del nodo
        self.txtTitle.setDefaultTextColor(Qt.GlobalColor.white)
        self.defineTextPosition()
        self.txtTitle.setZValue(2)

    def defineTextPosition(self):
        if not self.isTxtReversed:
            x = self.txtTitle.boundingRect().width()
            if "In" in self.plugData.className:
                x = (x * -1) - 5
            elif "Out" in self.plugData.className:
                x = 10
            self.txtTitle.setPos(x, -10)
        else:
            x = self.txtTitle.boundingRect().width()
            y = 0
            if "In" in self.plugData.className:
                x = 10
                self.txtTitle.setPos(x, -10)
            elif "Out" in self.plugData.className:
                x = (x * -1) - 5
                y = -10
                self.txtTitle.setPos(x, y)
        self.update()

    def updateTitle(self):
        self.txtTitle.setPlainText(self.title)
        self.defineTextPosition()

    def center(self):
        return self.mapToScene(self.boundingRect().center())

    def boundingRect(self):
        return self.boundingRectangle.normalized()

    def paint(self, painter, option, widget=None):
        # Draw the plugs
        painter.setBrush(Qt.GlobalColor.white)
        if not self.isSelected():
            painter.setPen(Qt.GlobalColor.black)
        else:
            painter.setPen(Qt.GlobalColor.red)
        _centerPoint = QPoint(self.diameter // 2, self.diameter // 2)
        painter.drawEllipse(_centerPoint, self.diameter, self.diameter)
        # draw the center  of the circle
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.black)
        _radius = self.diameter // 2
        painter.drawEllipse(_centerPoint, 3, 3)

    def contextMenuEvent(self, event: 'QGraphicsSceneContextMenuEvent') -> None:
        if not self.nodeInterface.isEditable:
            return
        menu = QMenu()
        actionRename = menu.addAction("Enable ReTitle")
        actionDelete = menu.addAction("Delete")
        actionUnlock = (
            menu.addAction("Unlock") if self.isLocked else menu.addAction("Lock")
        )
        if actionRename == menu.exec_(event.screenPos()):
            self.rename()
        elif actionDelete == menu.exec_(event.screenPos()):
            self.delete()
        elif actionUnlock == menu.exec_(event.screenPos()):
            self.unlock()

    def rename(self):
        """
        This method is called when the user right click on the plug and select the rename option.
        Is possibile to rename the plug only if the biggusNode is in editing mode. If you enable
        :return:
        """
        self.isGraphicalRenamePermitted = not self.isGraphicalRenamePermitted
        if self.isGraphicalRenamePermitted:
            self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        else:
            self.txtTitle.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

    def delete(self):
        self.nodeInterface.deletePlug(self)

    def unlock(self):
        if self.isLocked:
            self.isLocked = False
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        else:
            self.isLocked = True
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)

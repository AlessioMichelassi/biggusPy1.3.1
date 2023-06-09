from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.elements.Connections.Arrow import Arrow
from BiggusMain.elements.Connections.Connection import Connection
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeGraphicV1_2 import AbstractNodeGraphic
from BiggusMain.elements.Plugs.PlugGraphic import PlugGraphic
from BiggusMain.biggusWidgets.NodeFinderWidget import NodeFinderWidget


class GraphicViewOverride(QGraphicsView):
    # Variables
    isTabWindowsOpen: bool = False

    # Objects variables
    isConnectingPlug = False
    arrow: Arrow = None
    isOnCollision = False
    # Mouse variables
    isMiddleMouseButtonPressed = False
    lastMiddleMousePosition = None
    selectedItem = None
    lastSelectedItem = None
    # signal to update the position of the mouse in the status bar
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, canvas, graphicScene, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.graphicScene = graphicScene
        self.setScene(self.graphicScene)
        self.setRenderProperties()
        self.centerOn(80, 90)
        self.scaleScene(2)
        self.setAcceptDrops(True)

    def setRenderProperties(self):
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    # ------------------ MOUSE OVERRIDES ------------------

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            # determina se il doppio click è avvenuto all'interno del nodo
            pos = event.pos()
            if self.selectedItem is not None:
                if isinstance(self.selectedItem, AbstractNodeGraphic):
                    self.selectedItem.mouseDoubleClickEvent(event)
                elif isinstance(self.selectedItem, QGraphicsProxyWidget):
                    try:
                        self.selectedItem.widget().showToolBox(self.mapToScene(event.pos()))
                    except AttributeError as e:
                        print(e)
                super().mouseDoubleClickEvent(event)
            else:
                print("double click outside a biggusNode")
        super().mouseDoubleClickEvent(event)

    def wheelEvent(self, event):
        # sourcery skip: assign-if-exp
        """
        Override the wheel event to zoom in and out the scene
        :param event:
        :return:
        """
        if self.selectedItem is None:
            delta = event.angleDelta().y()
            self.scaleScene(1.5 ** (delta / 240.0))
        elif isinstance(self.selectedItem, QGraphicsProxyWidget):
            try:
                self.selectedItem.widget().wheelEvent(event)
                return
            except AttributeError as e:
                delta = event.angleDelta().y()
                self.scaleScene(1.5 ** (delta / 240.0))

    def scaleScene(self, scaleFactor):
        """
        Scale the scene
        :param scaleFactor:
        :return:
        """
        currentScale = self.transform().m11()
        if 0.13 < currentScale < 15:
            self.scale(scaleFactor, scaleFactor)
        elif currentScale <= 0.13:
            self.scale(0.2 / currentScale, 0.2 / currentScale)
        else:
            self.scale(0.8, 0.8)

    def panTheScene(self, event):
        # panning the scene!
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        currentPosition = event.pos()
        deltaPosition = currentPosition - self.lastMiddleMousePosition
        self.lastMiddleMousePosition = currentPosition
        hsBarValue = self.horizontalScrollBar().value()
        self.horizontalScrollBar().setValue(int(hsBarValue - (deltaPosition.x())))
        vsBarValue = self.verticalScrollBar().value()
        self.verticalScrollBar().setValue(int(vsBarValue - (deltaPosition.y())))
        event.accept()

    def centerObjectOnView(self, selectedObject=None):
        """
        ITA:
            Centra un oggetto nella scena. Se non viene passato nessun oggetto, ma
            sono presenti degli oggetti non selezionati, crea un rettangolo contenente tutti gli oggetti
            non selezionati event centra la scena su questo rettangolo, altrimenti centra la scena sul punto (0,0)
        ENG:
            Center an object in the scene. If no object is passed, but there are
            objects that are not selected, create a rectangle containing all the objects
            not selected and center the scene on this rectangle, otherwise center the scene on the point (0,0)
        :param selectedObject:
        :return:
        """
        if selectedObject is None:
            self.selectAllCenterSceneAndDeselect()
            return
        self.centerOn(selectedObject)
        self.scaleScene(1)

    def centerViewOnScene(self):
        """
        ITA:
            Centra la scena nella view
        ENG:
            Center the scene in the view
        :return:
        """
        if self.graphicScene.items():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.centerOn(self.sceneRect().center())

    def selectAllCenterSceneAndDeselect(self):
        """
        ITA:
            Seleziona tutti gli oggetti nella scena, centra la scena su uno di questi oggetti, la
            scala in modo che tutti gli oggetti siano visibili event deseleziona tutti gli oggetti
        ENG:
            Select all the objects in the scene, center the scene on one of these objects, scale it
            so that all objects are visible and deselect all objects.
        :return:
        """
        for item in self.graphicScene.items():
            item.setSelected(True)
        objsRect = self.graphicScene.itemsBoundingRect()
        self.fitInView(objsRect, Qt.AspectRatioMode.KeepAspectRatio)
        for item in self.graphicScene.items():
            item.setSelected(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        mousePosition = self.mapToScene(event.pos())
        self.scenePosChanged.emit(int(mousePosition.x()), int(mousePosition.y()))
        if self.isMiddleMouseButtonPressed:
            self.panTheScene(event)
        if self.isConnectingPlug:
            self.arrow.updatePosition(self.mapToScene(event.pos()))
        if event.buttons() == Qt.MouseButton.LeftButton:
            if isinstance(self.selectedItem, AbstractNodeGraphic):
                # se è premuto CTRL
                if QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
                    self.checkCollisions(self.selectedItem, event)

    def checkCollisions(self, node, event):
        if node == self.lastSelectedItem:
            return
        for item in self.graphicScene.items():
            if isinstance(item, Connection):
                if item.collidesWithItem(node):
                    self.isOnCollision = True
                    # crea una connessione fra i tre elementi
                    inputNode = item.inputNode
                    inputPlug = item.inputPlug.plugGraphic
                    inputIndexPlug = item.inIndex
                    self.checkIf_InPlug_IsConnected(inputPlug, event)
                    newNode = node.nodeData
                    newNodeOutPlug = newNode.outPlugs[0].plugGraphic
                    newNodeInPlug = newNode.inPlugs[0].plugGraphic
                    outputNode = item.outputNode
                    outputPlug = item.outputPlug.plugGraphic
                    outputIndexPlug = item.outIndex
                    self.createArrowFromTwoPlug(outputPlug, newNodeInPlug, event)
                    self.createArrowFromTwoPlug(newNodeOutPlug, inputPlug, event)
                    allItemIntheScene = self.graphicScene.items()
                    for item in allItemIntheScene:
                        if isinstance(item, Arrow):
                            self.graphicScene.removeItem(item)
                    self.lastSelectedItem = self.selectedItem

    def setConnection(self, connection):
        connection.outputNode.outConnections.append(connection)
        connection.inputNode.inConnections = connection
        self.canvas.connections.append(connection)
        self.graphicScene.addItem(connection)

    # -------------------------- MOUSE EVENTS -------------------------- #

    def leftMouseButtonPress(self, event):
        """
        ITA:
            Per prima cosa controlla se il click è stato effettuato su un oggetto
            event lo mette nella variabile self.selectedItem. Se il click è stato effettuato
            su un plug si sta tentando di connettere due nodi, quindi crea la freccia.
            Un plugOut può avere più collegamenti, un plugIn no, quindi prima di creare
            la freccia controlla se il plugIn non abbia già una connessione. In caso la cancella.
        ENG:
            First of all, it checks if the click was made on an object  and puts it in the variable self.selectedItem.
            If the click was made on a plug, you are trying to connect two nodes, so it creates the arrow.
            A plugOut can have more connections, a plugIn no, so before creating the arrow it checks if the plugIn
            does not already have a connection. In case it deletes it.
        :param event:
        :return:
        """
        self.selectedItem = self.getItemAtClick(event)
        if self.selectedItem is None:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        else:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
        if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
            print(self.selectedItem)
        elif isinstance(self.selectedItem, PlugGraphic):
            if "In" in self.selectedItem.name:
                plugGraphic = self.selectedItem
                # controlla se il plug di "In" non abbia connessioni
                self.checkIf_InPlug_IsConnected(plugGraphic, event)
            if not self.arrow:
                self.createArrow(event)

    def leftMouseButtonRelease(self, event):
        """
        ITA:
            Se si sta creando una connessione tra due nodi, controlla se il click è stato effettuato su un plug
            event se è un plug di "In" controlla se il plug non abbia già una connessione. In caso la cancella.
        ENG:
            If you are creating a connection between two nodes, check if the click was made on a plug
            and if it is a plug of "In" check if the plug does not already have a connection. In case it deletes it.
        :param event:
        :return:
        """
        item = self.getItemAtClick(event)
        if self.isConnectingPlug:
            if isinstance(item, PlugGraphic):
                self.connectNode(item, event)
            self.graphicScene.removeItem(self.arrow)
            self.arrow = None
            self.isConnectingPlug = False

    def middleMouseButtonPress(self, event):
        self.isMiddleMouseButtonPressed = True
        self.lastMiddleMousePosition = event.pos()
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def middleMouseButtonRelease(self, event):
        self.isMiddleMouseButtonPressed = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def getItemAtClick(self, event):
        """
        ITA:
            Ritorna l'oggetto cliccato
        ENG:
            Returns the clicked object
        :param event:
        :return:
        """
        return self.itemAt(event.pos())

    # -------------------------- DRAG OBJECT EVENTS -------------------------- #

    """    def dragEnterEvent(self, event):
            # se il drag and drop parte da un'altro widget
    
            if event.mimeData():
                event.acceptProposedAction()
    
        def dropEvent(self, event: QDropEvent):
            # sourcery skip: use-named-expression
            if event.mimeData():
                position = self.mapToScene(event.pos())
                mimeText = (event.mimeData().text()).split(";;")
                nodeName = mimeText[1]
                nodeAbsolutePath = mimeText[0]
                node = self.canvas.createNodeFromAbsolutePath(nodeAbsolutePath, nodeName)
                if node:
                    self.canvas.addNode(node)
                    node.setPos(position)  # posiziona il nodo nella scena"""

    # ---------------------- Connection  ----------------------

    def createArrow(self, event):
        """
        ITA:
            Crea la freccia che collega due nodi. La freccia è una specie di collegamento
            temporaneo event serve solo per visualizzare l'azione del collegare. Quando viene
            fatto il release del mouse viene creata la connessione vera event propria la freccia
            viene cancellata event sostituita con una Connection.
        ENG:
            Creates the arrow that connects two nodes. The arrow is a kind of temporary connection
            and is only used to visualize the action of connecting. When the mouse is released,
            the real connection is created, the arrow is deleted and replaced with a Connection.

        :param event:
        :return:
        """
        self.isConnectingPlug = True
        self.arrow = Arrow(self.selectedItem, self.mapToScene(event.pos()))
        self.graphicScene.addItem(self.arrow)

    def createArrowFromTwoPlug(self, plugOut, plugIn, event):
        """
        ITA:
            Crea la freccia che collega due nodi. La freccia è una specie di collegamento
            temporaneo event serve solo per visualizzare l'azione del collegare. Quando viene
            fatto il release del mouse viene creata la connessione vera event propria la freccia
            viene cancellata event sostituita con una Connection.
        ENG:
            Creates the arrow that connects two nodes. The arrow is a kind of temporary connection
            and is only used to visualize the action of connecting. When the mouse is released,
            the real connection is created, the arrow is deleted and replaced with a Connection.

        :param plugOut:
        :param plugIn:
        :param event:
        :return:
        """
        self.isConnectingPlug = True
        self.arrow = Arrow(plugIn, self.mapToScene(event.pos()))
        self.graphicScene.addItem(self.arrow)
        connection = self.arrow.establishConnection(plugOut)
        self.graphicScene.removeItem(self.arrow)
        self.arrow = None
        self.isConnectingPlug = False
        if connection:
            connection.outputNode.outConnect(connection)
            connection.inputNode.inConnect(connection)
            self.canvas.connections.append(connection)

    def createArrowFromConnection(self, connection, event):
        """
        ITA:
            Quando un nodo ha già una connessione in input, event si clicca sul suo plugIn,
            viene creata una freccia che collega il nodo con il nodo precedente in modo che la
            connessione possa essere modificata agevolmente.
        ENG:
            When a node already has an input connection, and you click on its plugIn,
            an arrow is created that connects the node with the previous node so that the
            connection can be easily modified.
        :param connection:
        :param event:
        :return:
        """
        self.isConnectingPlug = True
        self.arrow = Arrow(connection.outputPlug.plugGraphic, self.mapToScene(event.pos()))
        self.graphicScene.addItem(self.arrow)

    def checkIf_InPlug_IsConnected(self, item: PlugGraphic, event):
        """
        ITA:
            Controlla se il plug di "In" non abbia connessioni. Se ha una connessione la cancella.
        ENG:
            Checks if the plug of "In" does not have connections. If it has a connection, it deletes it.
        :param event:
        :param item:
        :return:
        """
        if item.plugData.inConnection is not None:
            connection = item.plugData.inConnection
            outNode = connection.outputNode
            for conn in outNode.outConnections:
                if conn and conn == connection:
                    conn.disconnect()
                    self.graphicScene.removeItem(conn)
                    self.canvas.connections.remove(conn)

            if not self.arrow and not self.isConnectingPlug:
                self.createArrowFromConnection(connection, event)

    def connectNode(self, plug: 'plugGraphic', event):
        # sourcery skip: use-named-expression
        """
        ITA:
            Connette insieme due plug.
            Se il plug In ha già una connessione, la sostituisce con la nuova.
        ENG:
            Connects two plugs together.
            If the In plug already has a connection, it replaces it with the new one.
        :param event:
        :param plug: il plug Out
        """
        # controlla se il plug di "In" non abbia connessioni
        self.checkIf_InPlug_IsConnected(plug, event)
        # quindi connette i plug se è possibile connetterli
        connection = self.arrow.establishConnection(plug)
        if connection:
            connection.outputNode.outConnect(connection)
            connection.inputNode.inConnect(connection)
            self.canvas.connections.append(connection)

    # --------------------- NODES EVENTS ---------------------

    def selectAllItems(self):
        for item in self.graphicScene.items():
            item.setSelected(True)

    def deleteSelectedItems(self):
        try:
            for item in self.graphicScene.selectedItems():
                if isinstance(item, AbstractNodeGraphic):
                    self.canvas.deleteNode(item.nodeInterface)
                elif isinstance(item, Connection):
                    self.canvas.deleteConnection(item)
                if item in self.graphicScene.items():
                    self.graphicScene.removeItem(item)
        except Exception as e:
            print(f"Debug From deleteSelectedItems: {e}")

    def disableNode(self):
        for item in self.graphicScene.selectedItems():
            if isinstance(item, AbstractNodeGraphic):
                item.nodeInterface.disable()

    def copyNode(self):
        self.canvas.clipboard.clear()
        itemToCopy = []
        for item in self.graphicScene.selectedItems():
            if isinstance(item, AbstractNodeGraphic):
                itemToCopy.append(item.nodeInterface)
        if itemToCopy:
            self.canvas.copyNode(itemToCopy)

    def pasteNode(self):
        self.canvas.pasteNode()

    # --------------------- TAB WINDOWS ---------------------

    def openTabWindow(self):
        """
        ITA:
            La tab Windows è una finestra di dialogo che serve per cercare i nodi event inserirli nella view.
        ENG:
            The tab Windows is a dialog window that is used to search for nodes and insert them into the view.
        :return:
        """
        centerPoint = self.mapToScene(self.viewport().rect().center())
        dialog = NodeFinderWidget(self.canvas, self, centerPoint, self)
        rect = self.canvas.geometry()
        _center = rect.center()
        x = _center.x()
        y = _center.y()
        dialog.move(int(x), int(y))
        dialog.show()

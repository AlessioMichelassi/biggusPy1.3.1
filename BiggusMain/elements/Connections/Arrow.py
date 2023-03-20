from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BiggusMain.elements.Connections.Connection import Connection

"""
Arrow è un oggetto grafico che rappresenta una connessione tra un plug e un punto nello schermo. 
Avviene quando si vuole creare una connessione fra due nodi, è in pratica solo un effetto visivo, ma quando
si rilascia il mouse su un plug viene creata una connessione vera e propria.
C'è una funzione di controllo per evitare che si colleghini IN con IN e OUT con OUT, o che si 
colleghino due plug dello stesso nodo.

Arrow is a graphic object that represents a connection between a plug and a point on the screen.
It happens when you want to create a connection between two nodes, it is basically just a visual effect, but when
the mouse is released on a plug a real connection is created.
There is a check function to avoid connecting IN with IN and OUT with OUT, or connecting two plugs of the same node.
"""


class Arrow(QGraphicsItem):
    currentNode = None

    def __init__(self, startPlug: 'PlugGraphic', end_point, parent=None):
        """
        ITA:
            Crea un oggetto grafico che rappresenta una freccia che collega un plug con un punto nello schermo.
            Viene creato quando si preme il mouse su un plug e viene trascinato fino a quando non viene rilasciato.
            Quando viene rilasciato viene creato un oggetto Connection che rappresenta la connessione vera e propria.
        ENG:
            Creates a graphic object that represents an arrow that connects a plug with a point on the screen.
            It is created when you press the mouse on a plug and drag it until it is released.
            When released, a Connection object is created that represents the actual connection.
        :param startPlug: the graphicPlug that is the start of the connection
        :param end_point: generally event.pos() when the mouse is clicked
        :param parent:
        """
        super().__init__(parent)

        self.startPlug = startPlug
        self.endPlug = None
        # startPoint è il centro del plug
        self.startPoint = startPlug.scenePos()
        self.endPoint = end_point
        self.setZValue(-100)

    def updatePosition(self, pos):
        """
        ITA:
            Aggiorna la posizione della freccia. Avviene quando si muove il mouse prima di rilasciarlo.
        ENG:
            Updates the position of the arrow. It happens when you move the mouse before releasing it.
        :param pos:
        :return:
        """
        self.endPoint = pos
        self.update()

    def establishConnection(self, endPlug: 'PlugGraphic'):
        """
        ITA:
            Crea una Connection o Edge fra due nodi. Viene chiamata quando si rilascia il mouse su un plug.
            Controlla che la connessione sia possibile, se lo è crea una nuova freccia e la aggiunge alla scena.
        ENG:
            Creates a Connection or Edge between two nodes. It is called when the mouse is released on a plug.
            Checks if the connection is possible, if it is creates a new arrow and adds it to the scene.
        :param endPlug:
        :return:
        """
        if self.checkIfConnectionIsPossible(endPlug):
            # controlla che lo start plug sia di Out altrimenti inverte i nodi
            if self.startPlug.name == "Out":
                # Crea una nuova freccia
                outputNode = self.startPlug.nodeGraphic.nodeData
                outputPlug = self.startPlug.plugData
                inputNode = endPlug.nodeGraphic.nodeData
                inputPlug = endPlug.plugData
            else:
                # Crea una nuova freccia
                outputNode = endPlug.nodeGraphic.nodeData
                outputPlug = endPlug.plugData
                inputNode = self.startPlug.nodeGraphic.nodeData
                inputPlug = self.startPlug.plugData
            conn = Connection(outputNode, outputPlug, outputPlug.index, inputNode, inputPlug, inputPlug.index)
            # Aggiungi la freccia alla scena
            self.scene().addItem(conn)
            return conn

    def checkIfConnectionIsPossible(self, endPlug: 'PlugGraphic'):
        """
        ITA:
            Controlla se la connessione è possibile.
            Una connessione è possibile se i due plug sono di sue nodi diversi
            event se i plug non sono dello stesso seme: In con In o Out con Out
        ENG:
            Check if the connection is possible.
            A connection is possible if the two plugs are of different nodes
            even if the plugs are not of the same seed: In with In or Out with Out
        :param endPlug: Plug di destinazione
        """
        # check if they are from the same node
        if self.startPlug.nodeInterface == endPlug.nodeInterface:
            print(f"startPlug: {self.startPlug.nodeInterface.getTitle()} result == endPlug: {endPlug.nodeInterface.getTitle()}")
            print("you can't connected plug of the same node")
            return False
        # check if they are of the same type
        elif self.startPlug.getClassName() == endPlug.getClassName():
            print(f"startPlug: {self.startPlug.getClassName()} result == endPlug: {endPlug.getClassName()}")
            print("you can't connected plug of the same type")
            return False
        else:
            return True

    def boundingRect(self):
        # Definiamo un bounding rectangle che include entrambe i punti della freccia
        return QRectF(self.startPoint, self.endPoint).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        """
        ITA:
            Disegna la freccia, in pratica una linea tratteggiata.
        ENG:
            Draws the arrow, basically a dashed line.
        :param painter:
        :param _QStyleOptionGraphicsItem:
        :param widget:
        :return:
        """
        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.DashLine))
        painter.drawLine(self.startPoint, self.endPoint)

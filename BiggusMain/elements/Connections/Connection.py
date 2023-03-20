import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsItem

from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeDataV1_2 import AbstractNodeData
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeGraphicV1_2 import AbstractNodeGraphic
from BiggusMain.elements.Nodes.AbstractClass.AbstractNodeInterfaceV1_2 import AbstractNodeInterface
from BiggusMain.elements.Plugs.PlugData import PlugData
from BiggusMain.elements.Plugs.PlugGraphic import PlugGraphic
from BiggusMain.elements.debugTool import debugTool


class Connection(QGraphicsItem, debugTool):
    outputNode = None
    outputPlug = None
    outIndex = None
    inputNode = None
    inputPlug = None
    inIndex = None

    def __init__(self, outputNode: AbstractNodeData, outputPlug: PlugData, outIndex,
                 inputNode: AbstractNodeData, inputPlug: PlugData, inIndex):
        """
        ITA:
            Costruttore della classe Connection. Una connection E' un edge tra l'output di un nodo e l'input di un altro nodo.
            e non viceversa. Questo perchE' il nodo che ha l'output puo' avere piu' di un input, ma un nodo che ha un input
            puo' avere solo un output. Inoltre, la classe funziona da observer, ossia quando viene modificato il valore
            di un nodo, viene aggiornato anche il valore di tutti i nodi che sono collegati a lui.
        ENG:
            Constructor of the Connection class. A connection is an edge between the output of a node and the input of another node.
            and not vice versa. This is because the node that has the output can have more than one input, but a node that has an input
            can only have one output. In addition, the class works as an observer, that is, when a node's value is modified, the value of all nodes
            that are connected to it is also updated.
        :param outputNode:
        :param outputPlug:
        :param outIndex:
        :param inputNode:
        :param inputPlug:
        :param inIndex:
        """
        super().__init__(className="Connection")
        self.setDebugMode(False)
        self.checkTheRightPlugType(outputNode, outputPlug, outIndex, inputNode, inputPlug, inIndex)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-100)

    def checkTheRightPlugType(self, outputNode, outputPlug, outIndex, inputNode, inputPlug, inIndex):
        """
        ITA:
            Questo metodo serve per controllare che il plug che viene passato come output sia effettivamente un output
            e non un input. Altrimenti inverte i parametri. Ritorna utile quando si connette un input a un output.
        ENG:
            This method is used to check that the plug that is passed as output is actually an output
            and not an input, otherwise it inverts the parameters. It is useful when connecting an input to an output.
        :param outputNode:
        :param outputPlug:
        :param outIndex:
        :param inputNode:
        :param inputPlug:
        :param inIndex:
        :return:
        """
        self.dPrint("checkTheRightPlugType", f"outNode:\n{outputNode}\ninNode\n{inputNode}")
        outputNode, outputPlug, inputNode, inputPlug = self.avoidTypeConfusion(outputNode, outputPlug,
                                                                               inputNode,inputPlug)
        if "Out" in outputPlug.className:
            self.outputNode = outputNode
            self.outputPlug = outputPlug
            self.outIndex = outIndex
            self.inputNode = inputNode
            self.inputPlug = inputPlug
            self.inIndex = inIndex
        elif "In" in inputPlug.className:
            self.outputNode = inputNode
            self.outputPlug = inputPlug
            self.outIndex = inIndex
            self.inputNode = outputNode
            self.inputPlug = outputPlug
            self.inIndex = outIndex

    @staticmethod
    def avoidTypeConfusion(outputNode, outputPlug, inputNode, inputPlug):
        """
        ITA:
            Questo metodo serve per evitare che il tipo di outputNode e inputNode sia di un tipo diverso da
            AbstractNodeData. Lo stesso controllo vine fatto per i plug.
        :param outputNode:
        :param outputPlug:
        :param inputNode:
        :param inputPlug:
        :return:
        """
        if isinstance(outputNode, (AbstractNodeInterface, AbstractNodeGraphic)):
            outputNode = outputNode.nodeData
        if isinstance(inputNode, (AbstractNodeInterface, AbstractNodeGraphic)):
            inputNode = inputNode.nodeData
        if isinstance(outputPlug, PlugGraphic):
            outputPlug = outputPlug.plugData
        if isinstance(inputPlug, PlugGraphic):
            inputPlug = inputPlug.plugData
        return outputNode, outputPlug, inputNode, inputPlug

    def __str__(self):
        return f"{self.outputNode.getTitle()}[{self.outputPlug.getTitle()}] -> [{self.inputPlug.getTitle()}]{self.inputNode.getTitle()}"

    def updateValue(self):
        """
        ITA:
            Questo metodo viene chiamato quando viene modificato il valore di un nodo. Il metodo chiama il calculate()
            del nodo di output, prende il valore e lo imposta come valore di input del nodo che ha l'input, quindi
            controlla le connessione del nodo di input e chiama il metodo updateValue() di ogni connessione. In questo
            modo viene aggiornato il valore di tutti i nodi che sono collegati a quello che ha subito la modifica.
        ENG:
            This method is called when a node's value is modified. The method calls the calculate ()
            of the output node, takes the value and sets it as the value of the input of the node that has the input,
            then checks the connections of the input node and calls the updateValue () method of each connection.
            In this way the value of all nodes that are connected together are updated.
        :return:
        """
        self.outputNode.calculate()
        value = self.outputNode.outPlugs[self.outIndex].getValue()
        self.inputNode.inPlugs[self.inIndex].setValue(value)
        self.inputNode.calculate()
        if self.inputNode.outConnections:
            for connection in self.inputNode.outConnections:
                connection.updateValue()

    def disconnect(self):
        """
        ITA:
            Questo metodo serve per disconnettere il nodo di output dal nodo di input. Il metodo viene chiamato quando
            viene eliminata la connessione. La connessione viene rimossa dalla lista delle connessioni del nodo e viene
            chiamato il metodo calculate() del nodo di output. Il modo da aggiornare il valore, Nel nodo di input
            invece viene richiamato il valore di parte di default del nodo.
        :return:
        """
        if self in self.inputNode.outConnections:
            self.inputNode.outConnections.remove(self)
        if self in self.outputNode.outConnections:
            self.outputNode.outConnections.remove(self)
        resetValue = self.inputNode.inPlugs[self.inIndex].getResetValue()
        self.inputNode.inPlugs[self.inIndex].setValue(resetValue)
        self.inputNode.calculate()
        if self.inputNode.outConnections:
            for connection in self.inputNode.outConnections:
                try:
                    connection.updateValue()
                except Exception as e:
                    # sometimes give an error when the connection is deleted
                    print(e)

    def boundingRect(self):
        return QRectF(self.outputPlug.plugGraphic.scenePos(), self.inputPlug.plugGraphic.scenePos()).normalized()

    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        if not self.isSelected():
            painter.setPen(QPen(QColor(0, 20, 20), 3))
        else:
            painter.setPen(QPen(QColor(250, 50, 50), 3))
        painter.drawLine(self.outputPlug.plugGraphic.center(), self.inputPlug.plugGraphic.center())

    def serialize(self):
        dicts = {
            'inputNodeName': self.inputNode.getTitle(),
            'inputPlug': self.inputPlug.index,
            'outputNodeName': self.outputNode.getTitle(),
            'outputPlug': self.outputPlug.index,
        }
        return json.dumps(dicts, indent=4)
